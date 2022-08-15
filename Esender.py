import smtplib
import socket, pyautogui
import streamlit as st
import mysql.connector
import os
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import xlrd
from testing import remove_string_part
st.set_page_config(page_title='Merge', page_icon='Merge_logo.png', initial_sidebar_state='expanded', )

# Main_button_design
Button_Design = st.markdown("""
<style>
div.stButton> button:first-child{
    color:  #1BA7B5;
    background: linear-gradient(to left,  #36363D,  #36363D,grey) right;
    background-size: 500%;
    transition: 0.3s ;
    border-radius:10px;
    font-size:22px;
    font-family: "Gill Sans", "Gill Sans MT", Calibri, "Trebuchet MS", sans-serif;
    position:relative;left:42%;
}
div.stButton:hover> button:first-child  {
    background-position: left;
    border-radius:40px;
    border-color:grey;
    color: white;
    font-size:22px;
    font-family: "Gill Sans", "Gill Sans MT", Calibri, "Trebuchet MS", sans-serif;
    position:relative;left:42%;
}
</style>""", unsafe_allow_html=True)

# Hide Streamlit Promotions
hide_streamlit_style = st.markdown("""
            <style>
            #MainMenu {visibility: visible;}
            footer {visibility: hidden;}
            footer {
                visibility: hidden;
            }
            footer:after {
                content:'Merge Sender 🖇️';
                visibility: visible;
                display: block;
                position: relative;
            }
            </style>
            """, unsafe_allow_html=True)

# Slang
st.markdown('''<div
  style="background-color:#36363D;padding:10px;border-radius:9px">
  <h1 
  style="color:black;font-size: 2.1vw;
  line-height: 1vw;
  margin:0;
  font-family: 'Red Hat Display', sans-serif;
  font-weight: 900;
  color: grey;">Merge Mail
  </h1> 
  </div> ''', unsafe_allow_html=True)
st.markdown('''<div
  style="background-color:#36363D;padding:10px;border-radius:9px">
  <h1
  style="
  font-size: .7vw;
  line-height: 1vw;
  margin: 0;
  font-family: 'Red Hat Display', sans-serif;
  font-weight: 900;
  color:grey ">-> Send mails to anyone,anyday
  </h1> 
  </div> ''', unsafe_allow_html=True)

st.text('')
hide_streamlita_style = """
<style>
.css-hi6a2p {padding-top: 0rem;}
</style>
"""
st.markdown(hide_streamlita_style, unsafe_allow_html=True)
# Connection to the MySQL Server
hostname = socket.gethostname()
mydb = mysql.connector.connect(host="localhost", user="root", password="amazing2002", database="email")
mycursor = mydb.cursor()

# Checking If already Logged in or not ( Switching page )
mycursor.execute(f"select * from info where hostname = '{hostname}' and status = 'active'")
check_log_or_sign = []
check_bool = False
name = ''
for i in mycursor:
    check_log_or_sign.append(i)

if check_log_or_sign != []:
    username_global = check_log_or_sign[0][1]
    for x in range(len(check_log_or_sign[0][1])):
        if check_log_or_sign[0][1][x] == '@':
            name = check_log_or_sign[0][1][0:x]
            break
    if name == '':
        name = check_log_or_sign[0][1]
    check_bool = True


# Login To your domain / mail Script.
def login():
    user = ''
    user_name_log = st.text_input('Username : ')
    password_log = st.text_input('Password : ', type='password')
    button_confirm = st.button('log in')
    st.error('your account will be stored unless you delete it!')

    if button_confirm:
        position_redirect = pyautogui.position()
        if not user_name_log and not password_log:
            st.info('-- Fields Empty --')

        if not password_log or not user_name_log:
            st.info('-- Field Empty --')

        if '.' not in user_name_log:
            st.info('-- Not valid format --')
        else:
            try:
                mycursor.execute(
                    f"select * from info where USERNAME = '{user_name_log}' and PASSWORD = '{password_log}'")
                check_exist = []
                for i in mycursor:
                    check_exist.append(i)
                if check_exist != []:
                    mycursor.execute(
                        f"update info set hostname = '{hostname}' where username = '{user_name_log}' and password = '{password_log}'")
                    mycursor.execute(f"update info set status = 'notactive' where hostname = '{hostname}'")
                    mycursor.execute(f"update info set status = 'active' where username = '{user_name_log}'")
                    mydb.commit()
                    st.success('--- Successfully logged in ---')
                    pyautogui.leftClick(position_redirect.x, position_redirect.y)
                else:
                    insert_state_sign = 'INSERT into INFO (USERNAME , PASSWORD,hostname,status) VALUES (%s,%s,%s,%s)'
                    rand, user = valid(user_name_log, password_log)
                    mycursor.execute(f"update info set status = 'notactive' where hostname = '{hostname}'")
                    status = 'active'
                    sign_up_values = (user_name_log, password_log, hostname, status)
                    mycursor.execute(insert_state_sign, sign_up_values)
                    mycursor.execute(
                        f'create table {user}emailstore (username varchar(100) not null,name_rec varchar(35) not null)')
                    mydb.commit()
                    st.success('--- Successfully logged in ---')
                    pyautogui.leftClick(position_redirect.x, position_redirect.y)
            except:
                st.info('Wrong username or password / less secure apps not turned on')


# Valid Email Script.
def valid(usern, passw):
    global user
    domain = ''
    for i in range(len(usern)):
        if usern[i] == '@':
            user = usern[0:i]
            for x in range(i, len(usern)):
                if usern[x] == '.':
                    domain = usern[i + 1:x]
                    break
    s = smtplib.SMTP(f'smtp.{domain}.com', 587)
    s.starttls()
    s.login(usern, passw)
    return domain, user


# Account Script.
def account():
    mycursor.execute(f"select username,password from info where username = '{username_global}'")
    account_info = []
    for i in mycursor:
        account_info.append(i)

    hidden_pass = ''
    length_pass = len(account_info[0][1]) - 3
    hidden_pass = account_info[0][1][0:3] + '*' * length_pass
    st.text('Username' + ': ' + account_info[0][0])
    st.text('Password' + ': ' + hidden_pass)
    if st.button('log out'):
        position_redirect = pyautogui.position()
        mycursor.execute(f"update info set status = 'notactive' where hostname = '{hostname}'")
        mydb.commit()
        st.success('-- Successfully logged out --')
        pyautogui.leftClick(position_redirect.x, position_redirect.y)
    delete_account()


# Sending Mail Script.
def send_mail(send):
    file_data_merge = st.file_uploader('Merge File',type=['xlsx'],accept_multiple_files=False)
    v1, v2 = st.beta_columns([1, 3])
    sub = v1.text_input('Subject')
    text_msg = st.text_area('', height=100,)
    file_upload = v2.file_uploader('Attachment', accept_multiple_files=True)
    b1,b2 = st.beta_columns([1,3])
    if not(file_data_merge):
        pass
    else:
        if b1.checkbox('Show Data'):
            mycursor.execute(f"select pathmerge from info where username = '{username_global}' and password = '{password}' and pathmerge != 'NULL'")
            check_cache = []
            for i in mycursor:
                check_cache.append(i)
            if not check_cache or check_cache[0][0].replace('__','\\').split('\\')[-1] != file_data_merge.name:
                with st.spinner('Extracting Data'):
                    path_merge = []
                    for root, dirs, files in os.walk(r'C:\\Users'):
                        for name in files:
                            if name == file_data_merge.name:
                                path_merge.append(os.path.abspath(os.path.join(root, name)))
                                break
                    path_merge = path_merge[0]
                    path_sql = path_merge.replace("\\", "__")
                    mycursor.execute(
                        f"update info set pathmerge = '{path_sql}' where username = '{username_global}' and password = '{password}'")
                    mydb.commit()

            elif check_cache[0][0].replace('__','\\').split('\\')[-1] == file_data_merge.name:
                path_merge = check_cache[0][0].replace("__","\\")


            input_workbook = xlrd.open_workbook(path_merge)
            input_worksheet = input_workbook.sheet_by_index(0)
            postion1,postion2 = st.beta_columns([1,4])
            expander_field_inputs = postion1.beta_expander('Field Inputs')
            if expander_field_inputs:
                merge_field_inputs = []
                for i in range(input_worksheet.ncols):
                    merge_field_inputs.append([])
                    for x in range(input_worksheet.nrows):
                        merge_field_inputs[i].append(input_worksheet.cell_value(x, i))
                show_xls_content = []
                for i in range(len(merge_field_inputs)):
                    show_xls_content.append(merge_field_inputs[i][0])
                for i in range(len(show_xls_content)):
                    expander_field_inputs.text('[['+show_xls_content[i]+']]')

            expander_show_file = postion2.beta_expander(f'{file_data_merge.name} File Content')
            if expander_show_file:
                merge_file_content_expander = []
                for i in range(input_worksheet.nrows):
                    merge_file_content_expander.append([])
                    for x in range(input_worksheet.ncols):
                        merge_file_content_expander[i].append(input_worksheet.cell_value(i, x))
                v = ''
                for i in range(len(merge_file_content_expander)):
                    for x in range(len(merge_file_content_expander[i])):
                        v+=str(merge_file_content_expander[i][x])+' '
                    expander_show_file.text(v)
                    v = ''

    if st.button('Send'):
        if text_msg == '':
            st.info('-- Field Empty --')
        elif send == []:
            st.info('-- Choose Contacts --')
        else:
            domain, rand = valid(username_global, password)
            s = smtplib.SMTP(f'smtp.{domain}.com', 587)
            send_to = []
            tex = []
            for i in range(len(send)):
                for x in range(0, len(send[i])):
                    if send[i][x] == ':':
                        send_to.append(send[i][0:x - 1])
                        tex.append(send[i][x + 2:])
            new = []
            path_merge = []
            if file_upload != '':
                for i in range(len(file_upload)):
                    for root, dirs, files in os.walk(r'C:\\Users'):
                        for name in files:
                            if name == file_upload[i].name:
                                new.append(os.path.abspath(os.path.join(root, name)))
                                break
            if file_data_merge:
                for root, dirs, files in os.walk(r'C:\\Users'):
                    for name in files:
                        if name == file_data_merge.name:
                            path_merge.append(os.path.abspath(os.path.join(root, name)))
                            break
                path_merge = path_merge[0]
                input_workbook = xlrd.open_workbook(path_merge)
                input_worksheet = input_workbook.sheet_by_index(0)
                merge_file_content = []
                for i in range(input_worksheet.ncols):
                    merge_file_content.append([])
                    for x in range(input_worksheet.nrows):
                        merge_file_content[i].append(input_worksheet.cell_value(x, i))
                if input_worksheet.nrows-1 < len(send_to):
                    st.info('xlsx file content less than the senders .')
                else:
                    print(merge_file_content)
                    rand = []
                    index = 0
                    for i in range(len(merge_file_content)):
                        if '[['+merge_file_content[i][0]+']]' in text_msg:
                            index+=1
                    if index == 0:
                        rand.append(text_msg)

                    else:
                        # Merge Replace Message Program
                        print(merge_file_content[0])
                        for x in range(1, len(merge_file_content[0])):
                            # Loop for replacing the template form to data
                            for j in range(index):
                                print(merge_file_content[j][0])
                                print(merge_file_content[j][x])
                                text_msg = text_msg.replace('[[' + merge_file_content[j][0] + ']]',
                                                            '[['+str(merge_file_content[j][x])+']]')
                            v1 = remove_string_part(text_msg,'[[')
                            v2 = remove_string_part(v1,']]')
                            rand.append(v2)
                            # # Loop for replacing the data to the original template for the next recipient to use
                            for n in range(index):
                                text_msg = text_msg.replace('[['+str(merge_file_content[n][x])+']]',
                                                            '[[' + merge_file_content[n][0] + ']]')

                    print('r', rand)
                    s.starttls()
                    s.login(username_global, password)
                    # Merge Core Program
                    for i in range(len(send_to)):
                        msg = MIMEMultipart()
                        msg['to'] = send_to[i]
                        msg['Subject'] = sub
                        msg.attach(MIMEText(rand[i]))
                        for path in new:
                            with open(path, "rb") as fil:
                                part = MIMEApplication(fil.read(), Name=basename(path))
                            # After the file is closed
                            part['Content-Disposition'] = 'attachment; filename="%s"' % basename(path)
                            msg.attach(part)
                        s.sendmail(username_global, send_to[i], str(msg))
                    st.success('-- Successfully sent --')
                    s.quit()

            else:
                s.starttls()
                s.login(username_global, password)
                for i in range(len(send_to)):
                    text_msg = text_msg.replace('[[name]]', tex[i])
                    msg = MIMEMultipart()
                    msg['to'] = send_to[i]
                    msg['Subject'] = sub
                    msg.attach(MIMEText(text_msg))
                    for path in new:
                        with open(path, "rb") as fil:
                            part = MIMEApplication(fil.read(), Name=basename(path))
                        # After the file is closed
                        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(path)
                        msg.attach(part)
                    s.sendmail(username_global, send_to[i], str(msg))
                    text_msg = text_msg.replace(tex[i], '[[name]]')
                st.success('-- Successfully sent --')
                s.quit()


# Adding Mail Contacts Script.
def add_contacts():
    emailname = st.text_input('Username (email)')
    add_name = st.text_input('Name (User)')
    if st.button('ADD'):
        check = False
        check_duplicate = []
        mycursor.execute(f'select * from {name}emailstore')
        for i in mycursor:
            check_duplicate.append(i)
        for i in range(len(check_duplicate)):
            if emailname == check_duplicate[i][0] or add_name == check_duplicate[i][1]:
                check = True
                break
        if not check:
            if emailname == '' or add_name == '':
                st.info('-- Fields Empty --')
            else:
                if '.' in emailname and '@' in emailname:
                    mycursor.execute(f"insert into {name}emailstore values('{emailname}','{add_name}')")
                    mydb.commit()
                    st.success('--- Added ---')
                else:
                    st.info('Enter a valid email')
        else:
            st.info('Already name/number Exists')


# Deleting Mail Contact Script.
def delete_email(contacts_to_delete):
    delete_name = []
    if st.button('Delete'):
        if contacts_to_delete == []:
            st.info('-- Choose Contacts --')
        else:
            for i in range(len(contacts_to_delete)):
                for x in range(0, len(contacts_to_delete[i])):
                    if contacts_to_delete[i][x] == ':':
                        delete_name.append(contacts_to_delete[i][0:x - 1])
            for i in delete_name:
                mycursor.execute(f"delete from {name}emailstore where username = '{i}'")
            mydb.commit()
            st.success('Successfully Deleted')


# Update Added Mail Contact Script
def update_name(name_selected):
    b1, b2 = st.beta_columns(2)
    update_mail = b1.text_input('New Email')
    update_name = b2.text_input('New Name')
    name_database = ''
    if b1.button('Change Mail name'):
        if name_selected is None:
            b1.info('-- Choose Contact --')
        elif update_mail == '':
            b1.info('-- Field Empty --')
        else:
            for i in range(len(name_selected)):
                if name_selected[i] == ':':
                    name_database = name_selected[0:i - 1]
            if '@' not in update_mail or '.' not in update_mail:
                b1.info('-- Enter a valid email address --')
            else:
                mycursor.execute(
                    f"update {name}emailstore set username = '{update_mail}' where username = '{name_database}' ")
                mydb.commit()
                b1.success('-- Successfully Updated --')
    if b2.button('Change Name'):
        if name_selected is None:
            b2.info('-- Choose Contact --')
        elif update_name == '':
            b2.info('-- Field Empty --')
        else:
            for i in range(len(name_selected)):
                if name_selected[i] == ':':
                    name_database = name_selected[0:i - 1]
            mycursor.execute(
                f"update {name}emailstore set name_rec = '{update_name}' where username = '{name_database}' ")
            mydb.commit()
            b2.success('-- Successfully Updated --')


# Displaying contacts Script.
def show_contacts_with_search():
    if select_box == 'Delete' or select_box == 'Send Mail':
        mycursor.execute(f"select * from {name}emailstore")
        contacts_data = []
        show_data = []
        v = 0
        for i in mycursor:
            contacts_data.append(i)
            show_data.append(contacts_data[v][0] + ' : ' + contacts_data[v][1])
            v += 1
        len_numbers = str(len(show_data))
        b1, b2 = st.beta_columns([4, 1])
        container = b1.beta_container()
        b2.text('')
        b2.text('')
        b2.text('')
        all = b2.checkbox("Select all")
        if all:
            select_search = container.multiselect('CONTACTS' + ' | ' + len_numbers + ' |', show_data, show_data)
        else:
            select_search = container.multiselect('CONTACTS' + ' | ' + len_numbers + ' |', show_data)
        return select_search
    else:
        mycursor.execute(f"select * from {name}emailstore")
        contacts_data = []
        show_data = ['']
        for i in mycursor:
            contacts_data.append(i)
        if contacts_data == []:
            select_search = st.selectbox('CONTACTS' + ' | ' + '0' + ' |', [])
        else:
            for i in range(len(contacts_data)):
                show_data.append(contacts_data[i][0] + ' : ' + contacts_data[i][1])
            len_numbers = str(len(show_data) - 1)
            select_search = st.selectbox('CONTACTS' + ' | ' + len_numbers + ' |', show_data)
        return select_search


# Permanent Delete Account Script.
def delete_account():
    if st.button('Delete Account'):
        mycursor.execute(f"drop table {name}emailstore")
        mycursor.execute(f"delete from info where username = '{username_global}'")
        mydb.commit()
        st.success('Successfully Deleted Account')


# Logged in
if check_bool:
    # User Password Used Everywhere.
    password = check_log_or_sign[0][2]
    # Making a Select box to switch between the Options.
    select_box = st.sidebar.selectbox('', ['Send Mail 📨', 'Add 🗒️', 'Delete 🚮', 'Update 📝', 'Account 👤','About 📜'])

    if select_box == 'Send Mail 📨':
        # Storing the return value from show_contacts_with_search module to "send to" variable , thus sending mails to the selected options.
        send_to = show_contacts_with_search()
        send_mail(send_to)

    elif select_box == 'Add 🗒️':
        show_contacts_with_search()
        add_contacts()

    elif select_box == 'Delete 🚮':
        # Storing the return value from show_contacts_with_search module to "which_contact" variable , thus Deleting Mail Contacts by knowing the selected options.
        which_contact = show_contacts_with_search()
        delete_email(which_contact)

    elif select_box == 'Update 📝':
        # Storing the return value from show_contacts_with_search module to "update_sel" variable , thus Updating Mail Contact by knowing the selected option to update.
        update_sel = show_contacts_with_search()
        update_name(update_sel)

    elif select_box == 'Account 👤':
        account()

    elif select_box == 'About 📜':
        # simple html code to make the page vibrant
        about_info1 = '''<div
                 style="background-image: linear-gradient(to right, #f63366, #fffd80);padding:2px;border-radius:9px">
                 </div> '''
        st.markdown(about_info1, unsafe_allow_html=True)

        # writing the text using html
        st.text('')
        about_info2 = '''<div
                 style="background-color:rgb(14, 17, 23);padding:2px;border-radius:9px">
                 <h2 
                 style="color:white;text-align:center;font-size:20px">DEVELOPER : AYAAN IZHAR
                 </h2> 
                 </div> '''
        st.markdown(about_info2, unsafe_allow_html=True)

# Not Logged in
else:
    st.markdown('>Log in to your domain')
    login()

