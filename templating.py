
order_codewords = ('Order',[
    ('%o','order_id','The Order id'),

    ])

client_codewords = ('Client',[

    ('%f','first_name','The Client\'s first name'),
    ('%l','last_name','The Client\'s last name'),
])



login_codewords = ('User',[
    ('%m','first_name','Your first name')
])

all_codewords = dict([order_codewords,client_codewords,login_codewords])

def replace(source_text,ob,table):
    '''Goes through the fields in a replacement table and subtitutes them into the source text'''
    for code,var,desc in table:
        #print code,var,desc
        val = getattr(ob,var)
        if(hasattr(val,'__call__')):
            val = val()

        source_text =  source_text.replace(code,val)

    return source_text


def fill_in_template(text,objs):
    '''replaces all the things in the soruce text with every object'''

    for obj in objs:
        if(obj != None):
            if(obj.__class__.__name__ in all_codewords):
                table = all_codewords[obj.__class__.__name__]
                text = replace(text,obj,table)

    return text

def populate_email(template,objs):
    '''Takes an email template, returns a subject/object mix with the fields filed in'''


    subject,body = replace_all(template.default_subject,objs),replace_all(template.text,objs)
    return [subject,body]

