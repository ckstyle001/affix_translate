import re
import os
import copy

for root, dirs, files in os.walk(os.path.join(os.getcwd(), 'Metadata')):
    for file in files:
        if file.endswith(".txt"):
            print(os.path.join(root, file))

            import_lines = []
            file_read_obj = open(os.path.join(root, file), "r", encoding="utf-16")  # 以只讀模式讀取檔案
            for i in file_read_obj:
                import_lines.append(i)  # 逐行將文字存入列表import_lines中
            file_read_obj.close()

            import_index = 0
            
            temp_dict = {}
            export_lines = []
            re.compile(r'[^\t\s]+.*')
            lang_list = ['"Russian"', '"Thai"', '"French"', '"German"', '"Spanish"', '"Korean"', '"Traditional Chinese"', '"Simplified Chinese"', '"Portuguese"']

            while import_index < len(import_lines):
                if import_lines[import_index].startswith('include') == True:
                    export_lines.append(import_lines[import_index])
                elif import_lines[import_index].startswith('no_description') == True:
                    export_lines.append(import_lines[import_index])
                elif import_lines[import_index].startswith('has_identifiers') == True:
                    export_lines.append(import_lines[import_index])
                elif import_lines[import_index].startswith('description') == True:
                    if len(temp_dict) > 0:
                        # "Traditional Chinese" content ---> content
                        if '"Traditional Chinese" lang' in temp_dict:
                            temp_dict['content'] = copy.deepcopy(temp_dict.get('"Traditional Chinese" content'))
                        
                        export_lines.append(temp_dict.get('title'))
                        export_lines.append(temp_dict.get('argument'))
                        while len(temp_dict.get('content')) > 0:
                            export_lines.append(temp_dict.get('content').pop(0))
                        for i in range(len(lang_list)):
                            if lang_list[i] + ' lang' in temp_dict:
                                export_lines.append(temp_dict.get(lang_list[i] + ' lang'))
                                while len(temp_dict.get(lang_list[i] + ' content')) > 0:
                                    export_lines.append(temp_dict.get(lang_list[i] + ' content').pop(0))
                        temp_dict.clear()
                    
                    temp_dict.update({'title': import_lines[import_index]})
                    import_index += 1
                    while import_index < len(import_lines):
                        if len(re.findall(r'[^\t\s]+.*', import_lines[import_index])) <= 0:
                            import_index += 1
                        else:
                            break
                    temp_dict.update({'argument': import_lines[import_index]})
                    import_index += 1
                    while import_index < len(import_lines):
                        if len(re.findall(r'[^\t\s]+.*', import_lines[import_index])) <= 0:
                            import_index += 1
                        else:
                            break
                    temp_list = []
                    temp_list.append(import_lines[import_index])
                    re_list = re.findall(r'\d+', import_lines[import_index])
                    for i in range(int(re_list[0])):
                        import_index += 1
                        while import_index < len(import_lines):
                            if len(re.findall(r'[^\t\s]+.*', import_lines[import_index])) <= 0:
                                import_index += 1
                            else:
                                break
                        temp_list.append(import_lines[import_index])
                    temp_dict.update({'content': temp_list})
                    del temp_list

                elif import_lines[import_index].find('lang "') >= 0:
                    re_list = re.findall(r'".*"', import_lines[import_index])
                    lang = re_list[0]
                    temp_dict.update({lang + ' lang': import_lines[import_index]})
                    import_index += 1
                    while import_index < len(import_lines):
                        if len(re.findall(r'[^\t\s]+.*', import_lines[import_index])) <= 0:
                            import_index += 1
                        else:
                            break
                    temp_list = []
                    temp_list.append(import_lines[import_index])
                    re_list = re.findall(r'\d+', import_lines[import_index])
                    # print(temp_dict)
                    for i in range(int(re_list[0])):
                        import_index += 1
                        while import_index < len(import_lines):
                            if len(re.findall(r'[^\t\s]+.*', import_lines[import_index])) <= 0:
                                import_index += 1
                            else:
                                break
                        temp_list.append(import_lines[import_index])
                    temp_dict.update({lang + ' content': temp_list})
                    del temp_list

                import_index += 1
                while import_index < len(import_lines):
                    if len(re.findall(r'[^\t\s]+.*', import_lines[import_index])) <= 0:
                        import_index += 1
                    else:
                        break

            if len(temp_dict) > 0:
                # "Traditional Chinese" content ---> content
                temp_dict['content'] = copy.deepcopy(temp_dict.get('"Traditional Chinese" content'))
                
                export_lines.append(temp_dict.get('title'))
                export_lines.append(temp_dict.get('argument'))
                while len(temp_dict.get('content')) > 0:
                    export_lines.append(temp_dict.get('content').pop(0))
                for i in range(len(lang_list)):
                    export_lines.append(temp_dict.get(lang_list[i] + ' lang'))
                    while len(temp_dict.get(lang_list[i] + ' content')) > 0:
                        export_lines.append(temp_dict.get(lang_list[i] + ' content').pop(0))
                temp_dict.clear()


            # 以寫的方式開啟檔案，如果檔案不存在，就會自動建立，如果存在就會覆蓋原檔案
            file_write_obj = open(os.path.join(root, file), 'w', encoding="utf-16")
            file_write_obj.writelines(export_lines)
            # for var in export_lines:
            #     file_write_obj.writelines(var)
            #     file_write_obj.writelines('\n')
            file_write_obj.close()
