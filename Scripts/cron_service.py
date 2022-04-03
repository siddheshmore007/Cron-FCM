from decouple import config
import mail_service


from json import JSONEncoder, JSONDecoder
from pymongo import MongoClient
import urllib
import razorpay


# Razorpay configurations
raz_client = razorpay.Client(auth=(config("RZP_TEST_KEY"), config("RZP_SECRET_KEY")))


# =======================================================
# MongoDB configurations
MONGO_DETAILS = config("MONGO_URL_BEG")+urllib.parse.quote_plus(config("MONGO_PWD"))+config("MONGO_URL_END")

my_client = MongoClient(MONGO_DETAILS)


# database
db = my_client["payments"]

# collections
collection = db["payments_collection"]
payment_status = db["status_collection"]


# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

def retrieve_new_payment_records():
    """
        This function retrieves new records added into the payment_collection
    """
    # only fetch records to which the payment link is yet to be shared
    # i.e. email_sent = False
    cursor = collection.find({"email_sent": False})
    payment_records = [record for record in cursor]

    return payment_records


def request_raz_link(name, mail_address, mobile):
    """
    This function returns razorpay links for each individual payment record
    :param name: full name of the student
    :param mail_address: mail address of the student
    :param mobile: mobile number of the student
    :return: Razorpay payment link for individual student
    """
    link = raz_client.payment_link.create({
        "amount": 500,
        "currency": "INR",
        "accept_partial": "false",
        "first_min_partial_amount": 100,
        "description": "For XYZ purpose",
        "customer": {
            "name": name,
            "email": mail_address,
            "contact": mobile
        },
        "notify": {
            "sms": "true",
            "email": "true"
        },

        "reminder_enable": "false",
        "notes": {
            "policy_name": "Enrollment Fees"
        },
        "callback_url": "https://www.fynd.academy/success-stories",
        "callback_method": "get"
    })

    # print(link)
    payment_link_id = link['id']
    rzp_link = link['short_url']
    pay_link_record = {"full_name": name, "email": mail_address, "payment_link_id": payment_link_id, "razorpay_link": rzp_link}
    payment_status.insert_one(pay_link_record)
    return link['short_url']



def request_links(payment_queue):
    for record in payment_queue:
        name = record["full_name"]
        mail_address = record["email"]
        student_id = record["student_id"]
        mobile = record["mobile_no"]
        # reference_id = record["reference_id"]
        link = request_raz_link(name, mail_address, mobile)
        # link = request_raz_link(name, mail_address, mobile, reference_id)
        mail_service.send_mail(name, mail_address, link)
        query = {"student_id": student_id}
        update_value = {"$set": {"email_sent": True}}
        collection.update_one(query, update_value)



if __name__ == "__main__":
    queue = retrieve_new_payment_records()
    print(queue)
    request_links(queue)

