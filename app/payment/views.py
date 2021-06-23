from flask import jsonify, render_template, request
from app.payment import payment_blueprint
from app import app
from app.customer.model import Customer
import stripe
import constants
from app.payment import utils
from app.customer.enums import PaymentStatusEnum

@payment_blueprint.route("/testingroute")
def testingRoute():
    return render_template('payment_index.html')

@payment_blueprint.route("/get_packages", methods = ["GET"])
def get_packages():
    packages = []
    for package in constants.payment_constants.OMS:
        packages.append(package)
    return jsonify({packages: packages}), 200

@payment_blueprint.route('/create-checkout-session', methods = ['POST'])
def create_checkout_session():
    data = request.json["customer_id"]
    c = Customer.query.get(data)
    if not c:
        return jsonify({"msg": "invalid customer id"}), 400

    customer = stripe.Customer.create(
        email = c.email_id,
        metadata = {
            "id": c.id
        }
    )
    session = stripe.checkout.Session.create(
        payment_method_types = constants.payment_constants.OMS['payment_method_types'],
        line_items=[{
        'price_data': {
            'currency': constants.payment_constants.OMS['currency'],
            'product_data': {
            'name': constants.payment_constants.OMS['description'],
            },
            'unit_amount': constants.payment_constants.OMS['cost'],
        },
        'quantity': constants.payment_constants.OMS['quantity'],
        }],
        customer= customer["id"],
        mode='payment',
        success_url='https://beehaz.com/payment/success',
        cancel_url='https://beehaz.com/payment/cancel',
    )

    return jsonify(id=session.id), 200

@payment_blueprint.route("/webhook", methods=["GET","POST"])
def stripe_weebhook():
    sig_header = request.headers["STRIPE_SIGNATURE"]
    try:
        event = stripe.Webhook.construct_event(request.data, sig_header, app.config['STRIPE_ENDPOINT_SECRET'])
    except ValueError as e:
        app.logger.error("exception while authenticating webhook: {e}".format(e = e))
        # Invalid payload
        return jsonify({"msg": "invalid payload"}), 400
    except stripe.error.SignatureVerificationError as e:
        app.logger.error("exception while authenticating webhook: {e}".format(e = e))
        # Invalid signature
        return jsonify({"msg": "invalid signature"}), 400
    
    updated_status = PaymentStatusEnum.UNPAID
    customer_id = -1
    
    # Handle the checkout.session.completed events
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
      
        app.logger.info("creating an order")
        updated_status = PaymentStatusEnum.PROCESSING
        customer_id = utils.get_customer_from_webhook_event(event)

        # Check if the order is already paid (e.g., from a card payment)
        #
        # A delayed notification payment will have an `unpaid` status, as
        # you're still waiting for funds to be transferred from the customer's
        # account.
        if session.payment_status == "paid":
            # Fulfill the purchase
            app.logger.info("fulfilling the order")
            updated_status = PaymentStatusEnum.MONTHLY_PAID

    # suceeded at a later stage
    elif event['type'] == 'checkout.session.async_payment_succeeded':
        session = event['data']['object']

        # Fulfill the purchase
        customer_id = utils.get_customer_from_webhook_event(event)
        updated_status = PaymentStatusEnum.MONTHLY_PAID

    elif event['type'] == 'checkout.session.async_payment_failed':
        session = event['data']['object']

        # Send an email to the customer asking them to retry their order
        customer_id = utils.get_customer_from_webhook_event(event)
        updated_status = PaymentStatusEnum.UNPAID
        app.logger.info("revert the state here and notify accordingly")
    if customer_id > 0:
        app.logger.info("here and customer id: " + str(customer_id) + " " + str(updated_status))
        utils.update_customer_payment_status(customer_id, updated_status)
    return jsonify({"msg": "success"}), 200