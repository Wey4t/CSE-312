def make_template(filename, data):
    with open(filename,"rb") as html_file:
        file_data = html_file.read().decode()
        file_data = replace_placeholders(file_data, data)
        file_data = replace_loop(file_data, data)
        return file_data
def replace_placeholders(file_data, data):
    replaced_file_data = file_data
    for placeholder in data.keys():
        if isinstance(data[placeholder], str):
            if data[placeholder] == None:
                replaced_file_data = (replaced_file_data.replace("{{"+placeholder+"}}", ''))
            else:
                replaced_file_data = (replaced_file_data.replace("{{"+placeholder+"}}", escape_html(data[placeholder])))
    return replaced_file_data
def replace_loop(file_data, data):
    final_content = file_data
    if 'loop_data' in data:
        for loop_data in data['loop_data']:
            loop_start_tag = loop_data['start_tag']
            loop_end_tag = loop_data['end_tag']
            start_index = file_data.find(loop_start_tag)
            if start_index == -1:
                continue
            end_index = file_data.find(loop_end_tag)
            loop_template = file_data[start_index+len(loop_start_tag): end_index]
            loop_data_1 =loop_data['datas']
            
            loop_contents = ''
            for single_content in loop_data_1:
            #print("replace:", single_content ,"template :",loop_template.encode())
                loop_contents += replace_placeholders(loop_template, single_content).strip('\n')
            final_content = file_data[ : start_index] + loop_contents + file_data[end_index+len(loop_end_tag):]
            file_data = final_content
    return final_content

def escape_html(input:str):
    return input.replace('&','&amp').replace('<','&lt').replace('>','&gt')
