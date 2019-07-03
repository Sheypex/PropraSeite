#! python3

import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def term_data(term, search):
    if not term.empty:
        #  data per hour (last 5 hours)
        term5 = term.index[-5].strftime('%Y-%m-%d %H:%M:%S') + ": " + str(term[-5])
        term4 = term.index[-4].strftime('%Y-%m-%d %H:%M:%S') + ": " + str(term[-4])
        term3 = term.index[-3].strftime('%Y-%m-%d %H:%M:%S') + ": " + str(term[-3])
        term2 = term.index[-2].strftime('%Y-%m-%d %H:%M:%S') + ": " + str(term[-2])
        term1 = term.index[-1].strftime('%Y-%m-%d %H:%M:%S') + ": " + str(term[-1])

        # Create the plain-text and HTML version of the message
        # Uses the 'term' variables to populate the file
        text = """\

            last Data retrieved per hour:
            {term_5}
            {term_4}
            {term_3}
            {term_2}
            {term_1}

            """.format(search=search, term_5=term5, term_4=term4, term_3=term3, term_2=term2, term_1=term1)

        html = """\
                <div>
                    <p>last Data retrieved per hour:</p>
                    <ul>
                        <li>{term_5}</li>
                        <li>{term_4}</li>
                        <li>{term_3}</li>
                        <li>{term_2}</li>
                        <li>{term_1}</li>
                    </ul>
                </div>      
            """.format(search=search, term_5=term5, term_4=term4, term_3=term3, term_2=term2, term_1=term1)

        logging.info('Term Data is ready!')
        return text, html
    else:
        return "", ""


def topuser_data(topuser):
    if not topuser.empty:
        # top users
        topuser1 = topuser.iloc[-1].User + ': ' + str(topuser.iloc[-1].Count)
        topuser2 = topuser.iloc[-2].User + ': ' + str(topuser.iloc[-2].Count)
        topuser3 = topuser.iloc[-3].User + ': ' + str(topuser.iloc[-3].Count)
        topuser4 = topuser.iloc[-4].User + ': ' + str(topuser.iloc[-4].Count)
        topuser5 = topuser.iloc[-5].User + ': ' + str(topuser.iloc[-5].Count)

        # Create the plain-text and HTML version of the message
        # Uses the 'topuser' to populate the file
        text = """\
            Top Users:
                {topuser_1}
                {topuser_2}
                {topuser_3}
                {topuser_4}
                {topuser_5}

            """.format(topuser_1=topuser1, topuser_2=topuser2, topuser_3=topuser3, topuser_4=topuser4,
                       topuser_5=topuser5)

        html = """\
                <div>
                    <p>Top Users:</p>
                    <ul>
                        <li>{topuser_1}</li>
                        <li>{topuser_2}</li>
                        <li>{topuser_3}</li>
                        <li>{topuser_4}</li>
                        <li>{topuser_5}</li>
                    </ul>
                </div>      
            """.format(topuser_1=topuser1, topuser_2=topuser2, topuser_3=topuser3, topuser_4=topuser4,
                       topuser_5=topuser5)

        logging.info('Top Users Data is ready!')
        return text, html
    else:
        return "", ""


def counted_data(counted):
    if not counted.empty:
        # top users
        counted1 = counted.iloc[-1].Term + ': ' + str(counted.iloc[-1].Anzahl)
        counted2 = counted.iloc[-2].Term + ': ' + str(counted.iloc[-2].Anzahl)
        counted3 = counted.iloc[-3].Term + ': ' + str(counted.iloc[-3].Anzahl)
        counted4 = counted.iloc[-4].Term + ': ' + str(counted.iloc[-4].Anzahl)
        counted5 = counted.iloc[-5].Term + ': ' + str(counted.iloc[-5].Anzahl)

        # Create the plain-text and HTML version of the message
        # Uses the 'counted' to populate the file
        text = """\
            Top Tweets counted:
                {counted_1}
                {counted_2}
                {counted_3}
                {counted_4}
                {counted_5}

            """.format(counted_1=counted1, counted_2=counted2, counted_3=counted3, counted_4=counted4,
                       counted_5=counted5)
        html = """\
                       <div>
                           <p>Top Tweets counted:</p>
                           <ul>
                               <li>{counted_1}</li>
                               <li>{counted_2}</li>
                               <li>{counted_3}</li>
                               <li>{counted_4}</li>
                               <li>{counted_5}</li>
                           </ul>
                       </div>      
            """.format(counted_1=counted1, counted_2=counted2, counted_3=counted3, counted_4=counted4,
                       counted_5=counted5)

        logging.info('Tweets counted Data is ready!')
        return text, html
    else:
        return "", ""


def has_data(term, topuser, sentiment, counted):
    #  TODO: include Sentiment
    if term.empty & topuser.empty & counted.empty:
        return False
    return True


def send_mail(subject, email, term, topuser, sentiment, counted, search):
    logging.warning("send_mail passed data: subject = "+subject+"; email = "+email+"; term = "+term+"; topuser = " + topuser + "; sentiment = "+sentiment+"; counted = "+counted+"; search ="+search)
    """
    sends an Email with the given subject, message_text and an html_elements version of the text
    """
    logging.info("Starting to compose the message to be send...")
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"  # service provider
    sender_email = "message.alert.system@gmail.com"  # Users address
    receiver_email = email  # receivers address
    password = "OneTwoThree"  # password

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email

    #  term data/hour -> last 5 hours loaded
    term_text, term_html = term_data(term, search)
    #  topuser data -> 5 top users shown
    topuser_text, topuser_html = topuser_data(topuser)
    #  tweets counted --> top 5 tweets
    counted_text, counted_html = counted_data(counted)

    text = """\

    This is an automatic message send from the message alert system. 
    The following summary contains information about the tweet: {search}
    {term_text}
    {topuser_text}
    {counted_text}



    """.format(search=search, term_text=term_text, topuser_text=topuser_text, counted_text=counted_text)

    # Create the plain-text and HTML version of the message
    # Uses the html element to populate the file
    html = """\
    <html>
      <body>
        <div>
        This is an automatic message send from the message alert system. 
        </div>
        <div>
        The following summary contains information about the tweet: {search}
        </div>

        {term_html}
        {topuser_html}
        {counted_html} 

      </body>
    </html>
    """.format(search=search, term_html=term_html, topuser_html=topuser_html, counted_html=counted_html)
    logging.info("Finished building the message to be send...")

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)
    if has_data(term, topuser, sentiment, counted):
        with smtplib.SMTP_SSL(smtp_server, port) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            logging.info("Successfully send email to: "+receiver_email)
    else:
        logging.warning("there was no data to be sent...")


logging.basicConfig(filename='logs.log', level=logging.DEBUG, format='%(asctime)s %(message)s')

__author__ = 'Cesar Mauricio Acuna Herrera'
