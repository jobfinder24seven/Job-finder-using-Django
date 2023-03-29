from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from random import randint
import math, random
import time
from datetime import datetime

currentYear = datetime.now().year

website_name = 'JobFinder'
support_team_name = 'Balikis Omolewa Nasiru'
version = f'2022 - {currentYear} JobFinder247'
username_ =  'admin'
first_name = username_
email_ = 'admin@jobfinder.com'
password_ = 'jf-admin'


LOCATION_CHOICES = ['-','Abia', 'Adamawa', 'Akwa Ibom', 'Anambra', 'Bauchi', 'Bayelsa', 'Benue', 'Borno', 'Cross River', 'Delta', 'Ebonyi', 'Edo',
                    'Ekiti', 'Enugu', 'FCT - Abuja', 'Gombe', 'Imo', 'Jigawa', 'Kaduna', 'Kano', 'Katsina', 'Kebbi', 'Kogi', 'Kwara', 'Lagos', 
                    'Nasarawa', 'Niger', 'Ogun', 'Ondo', 'Osun', 'Oyo', 'Plateau', 'Rivers', 'Sokoto', 'Taraba', 'Yobe', 'Zamfara']

COUNTRY_CHOICES = ["-","United States", "Canada", "Afghanistan", "Albania", "Algeria", "American Samoa", "Andorra", "Angola", "Anguilla", "Antarctica",
                   "Antigua and/or Barbuda", "Argentina", "Armenia", "Aruba", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh",
                   "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bermuda", "Bhutan", "Bolivia", "Bosnia and Herzegovina", "Botswana", "Bouvet Island", "Brazil", 
                   "British Indian Ocean Territory", "Brunei Darussalam", "Bulgaria", "Burkina Faso", "Burundi", "Cambodia", "Cameroon", "Cape Verde", "Cayman Islands", 
                   "Central African Republic", "Chad", "Chile", "China", "Christmas Island", "Cocos (Keeling) Islands", "Colombia", "Comoros", "Congo", "Cook Islands",
                   "Costa Rica", "Croatia (Hrvatska)", "Cuba", "Cyprus", "Czech Republic", "Denmark", "Djibouti", "Dominica", "Dominican Republic", "East Timor", "Ecuador", 
                   "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Ethiopia", "Falkland Islands (Malvinas)", "Faroe Islands", "Fiji", "Finland", "France",
                   "France, Metropolitan", "French Guiana", "French Polynesia", "French Southern Territories", "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Gibraltar", 
                   "Greece", "Greenland", "Grenada", "Guadeloupe", "Guam", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Heard and Mc Donald Islands", "Honduras", 
                   "Hong Kong", "Hungary", "Iceland", "India", "Indonesia", "Iran (Islamic Republic of)", "Iraq", "Ireland", "Israel", "Italy", "Ivory Coast", "Jamaica", "Japan",
                   "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Korea, Democratic People's Republic of", "Korea, Republic of", "Kuwait", "Kyrgyzstan", "Lao People's Democratic Republic", 
                   "Latvia", "Lebanon", "Lesotho", "Liberia", "Libyan Arab Jamahiriya", "Liechtenstein", "Lithuania", "Luxembourg", "Macau", "Macedonia", "Madagascar", "Malawi", "Malaysia", 
                   "Maldives", "Mali", "Malta", "Marshall Islands", "Martinique", "Mauritania", "Mauritius", "Mayotte", "Mexico", "Micronesia, Federated States of", "Moldova, Republic of", 
                   "Monaco", "Mongolia", "Montserrat", "Morocco", "Mozambique", "Myanmar", "Namibia", "Nauru", "Nepal", "Netherlands", "Netherlands Antilles", "New Caledonia", "New Zealand",
                   "Nicaragua", "Niger", "Nigeria", "Niue", "Norfolk Island", "Northern Mariana Islands", "Norway", "Oman", "Pakistan", "Palau", "Panama", "Papua New Guinea", "Paraguay", "Peru", 
                   "Philippines", "Pitcairn", "Poland", "Portugal", "Puerto Rico", "Qatar", "Reunion", "Romania", "Russian Federation", "Rwanda", "Saint Kitts and Nevis", "Saint Lucia", 
                   "Saint Vincent and the Grenadines", "Samoa", "San Marino", "Sao Tome and Principe", "Saudi Arabia", "Senegal", "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia",
                   "Solomon Islands", "Somalia", "South Africa", "South Georgia South Sandwich Islands", "Spain", "Sri Lanka", "St. Helena", "St. Pierre and Miquelon", "Sudan", "Suriname",
                   "Svalbard and Jan Mayen Islands", "Swaziland", "Sweden", "Switzerland", "Syrian Arab Republic", "Taiwan", "Tajikistan", "Tanzania, United Republic of", "Thailand", "Togo",
                   "Tokelau", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan", "Turks and Caicos Islands", "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates",
                   "United Kingdom", "United States minor outlying islands", "Uruguay", "Uzbekistan", "Vanuatu", "Vatican City State", "Venezuela", "Vietnam", "Virgin Islands (British)", 
                   "Virgin Islands (U.S.)", "Wallis and Futuna Islands", "Western Sahara", "Yemen", "Yugoslavia", "Zaire", "Zambia", "Zimbabwe"]

INDUSTRY_CHOICES = ['-','Accounting', 'Airlines/Aviation', 'Alternative Dispute Resolution', 'Alternative Medicine', 'Animation', 'Apparel & Fashion', 'Architecture & Planning', 'Arts & Crafts', 'Automotive',
                    'Aviation & Aerospace', 'Banking', 'Biotechnology', 'Broadcast Media', 'Building Materials', 'Business Supplies & Equipment', 'Capital Markets', 'Chemicals', 'Civic & Social Organization',
                    'Civil Engineering', 'Commercial Real Estate', 'Computer & Network Security', 'Computer Games', 'Computer Hardware', 'Computer Networking', 'Computer Software', 'Construction', 'Consumer Electronics', 
                    'Consumer Goods', 'Consumer Services', 'Cosmetics', 'Dairy', 'Defense & Space', 'Design', 'Education Management', 'E-learning', 'Electrical & Electronic Manufacturing', 'Entertainment', 'Environmental Services',
                    'Events Services', 'Executive Office', 'Facilities Services', 'Farming', 'Financial Services', 'Fine Art', 'Fishery', 'Food & Beverages', 'Food Production', 'Fundraising', 'Furniture', 'Gambling & Casinos', 
                    'Glass, Ceramics & Concrete', 'Government Administration', 'Government Relations', 'Graphic Design', 'Health, Wellness & Fitness', 'Higher Education', 'Hospital & Health Care', 'Hospitality', 'Human Resources',
                    'Import & Export', 'Individual & Family Services', 'Industrial Automation', 'Information Services', 'Information Technology & Services', 'Insurance', 'International Affairs', 'International Trade & Development',
                    'Internet', 'Investment Banking/Venture', 'Investment Management', 'Judiciary', 'Law Enforcement', 'Law Practice', 'Legal Services', 'Legislative Office', 'Leisure & Travel', 'Libraries', 'Logistics & Supply Chain', 
                    'Luxury Goods & Jewelry', 'Machinery', 'Management Consulting', 'Maritime', 'Marketing & Advertising', 'Market Research', 'Mechanical or Industrial Engineering', 'Media Production', 'Medical Device', 'Medical Practice',
                    'Mental Health Care', 'Military', 'Mining & Metals', 'Motion Pictures & Film', 'Museums & Institutions', 'Music', 'Nanotechnology', 'Newspapers', 'Nonprofit Organization Management', 'Oil & Energy', 'Online Publishing', 
                    'Outsourcing/Offshoring', 'Package/Freight Delivery', 'Packaging & Containers', 'Paper & Forest Products', 'Performing Arts', 'Pharmaceuticals', 'Philanthropy', 'Photography', 'Plastics', 'Political Organization', 'Primary/Secondary', 
                    'Printing', 'Professional Training', 'Program Development', 'Public Policy', 'Public Relations', 'Public Safety', 'Publishing', 'Railroad Manufacture', 'Ranching', 'Real Estate', 'Recreational', 'Facilities & Services', 'Religious Institutions',
                    'Renewables & Environment', 'Research', 'Restaurants', 'Retail', 'Security & Investigations', 'Semiconductors', 'Shipbuilding', 'Sporting Goods', 'Sports', 'Staffing & Recruiting', 'Supermarkets', 'Telecommunications', 'Textiles', 'Think Tanks', 
                    'Tobacco', 'Translation & Localization', 'Transportation/Trucking/Railroad', 'Utilities', 'Venture Capital', 'Veterinary', 'Warehousing', 'Wholesale', 'Wine & Spirits', 'Wireless', 'Writing & Editing']

JOB_TYPE_CHOICES = ['-','Full Time','Remote','Intership','Shift']

NUMBER_CHOICES= ['-','Less than 10','10 - 50','100 - 200','200 - 500','500 - 1000','More than 1000']

EXP_CHOICES = ['-','Less than 2yrs',
               '2yrs - 5yrs',
               '5yrs - 10yrs',
               '10yrs - 15yrs',
               'More than 15yrs']

GENDER_CHOICES = ['-','Male','Female','Others']
BOOLEAN_CHOICES = ['-','YES','NO']
 

QUALIFICATION_CHOICES=['-','First School Leaving Certificate','Secondary School (SSCE)',
                       'NCE','OND','BA/BSc/HND','MBA/MSc/MA','PhD/Fellowship','Vocational','others']

APPLICATION_CHOICES = ['-','Candidate should apply via company website',
                       'Candidate should send email via company email address',
                       'Candidate should apply with noraml application form',
                        ]

COMPANY_TYPE_CHOICES = ['-','Direct Employer','Recruitment Agency']

NOTIFICATION_CHOICES = ["Changes made to your account",
                        "Product updates for products you've purchased or starred",
                        "Information on new products and services",
                        "Marketing and promotional offers",
                        "Security alerts"
                        ]
def eToken(t=0):
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        #print(timer, end="\r")
        time.sleep(1)
        t -= 1
    return randint(100000,999999)
 
def username():
    string="0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

    lent = len(string)
    username = ""
    for x in range(8):
        username+=string[math.floor(random.random()*lent)]
            
    return f'JF{username}'
    
def send_html_email(request,template_name,content,subject,email_to,msg):
    #email_from= settings.EMAIL_HOST_USER

    # load html_contect"= render_to_string('template_name', {content_dics)
    
    html_content = render_to_string(template_name, content) 
    text_content = strip_tags(html_content)
        
    email_obj = EmailMultiAlternatives(subject,text_content,settings.EMAIL_HOST_USER,[email_to])
    email_obj.attach_alternative(html_content, 'text/html')
    email_obj.send()
    messages.success(request,msg)
    pass
        
def send_email_with_attachement(request,file_name,template_name,content,subject,email_to):

    html_content = render_to_string(template_name, content) 
    text_content = strip_tags(html_content)
    mail = EmailMultiAlternatives(subject,text_content,settings.EMAIL_HOST_USER,[email_to])
    if request.FILES:
        attachement= request.FILES[file_name] # file is the name value which you have provided in form for file field
        mail.attach(attachement.name, attachement.read(), attachement.content_type)
        mail.send()
        
        

    





  









