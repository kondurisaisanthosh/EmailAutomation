import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def read_properties(file_path):
    properties = {}
    with open(file_path, 'r') as file:
        for line in file:
            if '=' in line:
                key, value = line.strip().split('=', 1)
                properties[key.strip()] = value.strip()
    return properties

def getEmails():
    out = ["konduri.santhosh96@gmail.com","sandeep.konduri123@gmail.com", "saisanthoshkonduri@gmail.com","vamsi.gch@gmail.com", "goutham221997@gmail.com"]
    return out

def main():
    try:
        properties = read_properties('config.properties')

        # Email configuration
        sender_email = properties['email']
        password = properties['password']

        # Connect to the SMTP server.
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)

        receiver_emails = getEmails()
        for i in range(len(receiver_emails)):
            receiver_email = receiver_emails[i]

            # Create message container - the correct MIME type is multipart/alternative.
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['Subject'] = "Job Application: Java Full Stack Developer"
            msg['To'] = receiver_email

            # Create the body of the message (a plain-text and an HTML version).
            text = ""
            html = """\
                <html>
                      <body style = "color: black">
                            <p>Hello, </p>
                            <p> &emsp; I hope you are safe and doing well. My name is Santhosh Konduri, and I am writing to let you know about my interest in Java full-stack positions. As an accomplished Full Stack Java Developer with seven-plus years of experience designing, implementing, and maintaining robust software solutions, I am eager to contribute my skills and expertise to your esteemed organization. My background includes proficient utilization of frameworks and technologies such as Spring-boot, NodeJs, Angular, etc., enabling me to develop efficient, robust, and scalable applications.
                            <br>
                            &emsp; I am open to relocating to any place in the USA. Please find my employer details and resume attached, and let me know if you need anything.</p>
                            <p>

                            <b>Employer Details:</b>
                            <br>
                            Rahul Varma
                            <br>
                            Email: Rahul@sanquest.com
                            <br>
                            Sr. Talent Acquisition Specialist
                            <br>
                            SanQuest, Inc. | 713-400-1275 | 8411 Sterling St, Irving, TX 75063. </p>

                            <br>
                            <p>
                            <b>Thanks,</b>
                            <br>
                            Sai Santhosh
                            <br>
                            (720) 649- 6277
                            </p>      
                      </body>
                </html>
            """

            # Attachment file path
            attachment_path = "/Users/saisanthoshkonduri/Downloads/2024 marketing/sanquest/Sai Santhosh Konduri.docx"

            with open(attachment_path, "rb") as attachment:
                # Add file as application/octet-stream
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
            encoders.encode_base64(part)

            # Add header as key/value pair to attachment part
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {attachment_path.split('/')[-1]}",
            )
            # Attach both plain-text and HTML versions of the message
            part1 = MIMEText(text, 'plain')
            part2 = MIMEText(html, 'html')
            msg.attach(part1)
            msg.attach(part2)
            msg.attach(part)

            # send the email
            server.sendmail(sender_email, receiver_email, msg.as_string())
            print("Email sent successfully to", receiver_email)

    except Exception as e:
        print(e)
    finally:
        # Close the connection
        server.quit()

if __name__ == "__main__":
    main()


