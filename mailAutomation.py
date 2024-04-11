import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import pandas as pd
import time
import constants

def read_properties(file_path):
    properties = {}
    with open(file_path, 'r') as file:
        for line in file:
            if '=' in line:
                key, value = line.strip().split('=', 1)
                properties[key.strip()] = value.strip()
    return properties

def getEmails():
    out = {}
    excel_file = "vendor.xlsx"
    # Read Excel file into a pandas DataFrame
    df = pd.read_excel(excel_file, na_values=['', 'NA'])
    data_dict = df.to_dict(orient="records")
    for ele in data_dict:
        key = ele[constants.EMAIL]
        value =""
        if str(ele[constants.FIRST_NAME])!="nan":
            value += str(ele[constants.FIRST_NAME])+" "
        if str(ele[constants.LAST_NAME])!="nan":
            value += str(ele[constants.LAST_NAME])
        out[key]=value
    return out

def main():
    try:
        start_time = time.time()
        count=0
        properties = read_properties('config.properties')

        # Email configuration
        sender_email = properties[constants.EMAIL]
        password = properties[constants.PASSWORD]

        # Connect to the SMTP server.
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)

        receiver_emails = getEmails()
        for key, value in receiver_emails.items():
            count += 1
            receiver_email = key.strip()

            # Create message container - the correct MIME type is multipart/alternative.
            msg = MIMEMultipart()
            msg[constants.FROM] = sender_email
            msg[constants.SUBJECT] = "Passionate Java Developer Eager for New Opportunities"
            msg[constants.TO] = receiver_email

            # Create the body of the message (HTML version).
            html = """
                <html>
                      <body style = "color: black">
                            <p>
                                Hello {},
                            </p>
                            <p>
                                I hope you are safe and doing well. With over seven years of expertise as a Senior Software Fullstack developer, I bring a wealth of knowledge to the organization. I reside in Dallas, Texas. I am open to relocating to any place in the USA and remote opportunities.  
                            </p>
                            <p>
                                I am excited about contributing my skills and experience to your team. Could we schedule a discussion at your earliest convenience to explore this further?
                            </p>
                            
                            <p>
                                For your perusal, I have attached my resume for your reference.
                            </p>
                                                        
                            <p>
                                Best Regards,
                                <br>
                                Sai Santhosh
                                <br>
                                Email: kondurisanthosh500@gmail.com
                                <br>
                                Phone: (720) 649- 6277
                            </p>      
                      </body>
                </html>
            """.format(value)

            # Attachment file path
            attachment_path = "/Users/saisanthoshkonduri/Downloads/2024 marketing/sanquest/Sai Santhosh Konduri.docx"

            with open(attachment_path, "rb") as attachment:
                # Add file as application/octet-stream
                part2 = MIMEBase("application", "octet-stream")
                part2.set_payload(attachment.read())
            encoders.encode_base64(part2)

            # Add header as key/value pair to attachment part
            part2.add_header(
                "Content-Disposition",
                f"attachment; filename= {attachment_path.split('/')[-1]}",
            )
            # Attach both plain-text and HTML versions of the message
            part1 = MIMEText(html, 'html')
            msg.attach(part1)
            msg.attach(part2)

            # send the email
            server.sendmail(sender_email, receiver_email, msg.as_string())
            print("Email sent successfully to", receiver_email)
        end_time = time.time()
        total_time = end_time - start_time
        rounded_time = round(total_time, 3)
        print("Total time taken:", rounded_time, "seconds")
        print("Total No of Emails:", count)

    except Exception as e:
        print(e)
    finally:
        # Close the connection
        server.quit()

if __name__ == "__main__":
    main()

