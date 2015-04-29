def replace(source_text,ob,table):
    '''Goes through the fields in a replacement table and subtitutes them into the source text'''
    for code,var,desc in table:
        #print code,var,desc
        val = getattr(ob,var)
        if(hasattr(val,'__call__')):
            val = val()


        if(val != None):
            source_text =  source_text.replace(code,unicode(val))

    return source_text


def fill_in_template(text,objs):
    '''replaces all the things in the soruce text with every object'''

    for obj in objs:
        if(hasattr(obj,'template_codes')):
                table = obj.template_codes
                text = replace(text,obj,table)

    return text


def populate_email(template,objs):
    '''Takes an email template, returns a subject/object mix with the fields filed in'''
    subject,body = fill_in_template(template.default_subject,objs),fill_in_template(template.text,objs)
    return [subject,body]

