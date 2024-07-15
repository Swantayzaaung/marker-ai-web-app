import re
#input_arr = ['1', 'Bacteria are classified in the Prokaryote kingdom.', '(a)', 'State two features of animal cells that are not found in bacteria.', '1', '................................................................................................................................................', '2', '................................................................................................................................................ [2]', '(b)', 'The bacterium Bacillus megaterium was grown in the laboratory fermenter shown in Fig. 1.1.', 'air lock water sterile air magnetic stirrer bacteria, source of nitrogen and glucose', 'Fig. 1.1', '(i)', 'Explain why a source of nitrogen and glucose were added to the fermenter.', 'nitrogen ............................................................................................................................. ........................................................................................................................................... glucose .............................................................................................................................. ........................................................................................................................................... [2]', '(ii)', 'Suggest why it is important to stir the contents of the fermenter continuously.', '........................................................................................................................................... ........................................................................................................................................... ........................................................................................................................................... ........................................................................................................................................... ........................................................................................................................................... ........................................................................................................................................... ..................................................................................................................................... [3]', '(c)', 'Samples were taken from the fermenter at frequent intervals and the number of live bacteria was determined. The results are shown in Fig. 1.2.', '0 0 10 20 30 40 50 60 100 200 300 400 500 600 700 800 number of live bacteria / million per cm3 time /hours ABCDA B C D', 'Fig. 1.2', 'Describe and explain what happens to the number of live bacteria shown in the stages labelled A, B, C and D in Fig. 1.2.', '...................................................................................................................................................', '................................................................................................................................................... ................................................................................................................................................... ................................................................................................................................................... ................................................................................................................................................... ................................................................................................................................................... ................................................................................................................................................... ................................................................................................................................................... ................................................................................................................................................... ................................................................................................................................................... ................................................................................................................................................... ............................................................................................................................................. [6]', '[Total: 13]'] 
#input_arr = ['......', 'asdfasd', 'asdf ........', '.......... .........\
#...........', '.......... .........', '.......... ......', 'abasdf']
input_arr = ['3', 'Parity checks can be used to check for errors during data transmission.', 'One of the bytes has been transmitted incorrectly.', 'Byte 1', 'Byte 2', 'Byte 3', 'Byte 4', '10110011', '10101000', '10110100', '10110101', '(a)', 'State which byte was incorrectly transmitted.', '...............................................................................................................................................[1]', '(b)', 'Explain how you identified the incorrectly transmitted byte.', '................................................................................................................................................... ................................................................................................................................................... ................................................................................................................................................... ................................................................................................................................................... ...................................................................................................................................................', '...............................................................................................................................................[3]']
output_arr = []

def merge_blanks(array):
    output_arr = []
    blank_count = 0
    startIndex = -1
    
    question_no = array[0]
    sub_question = ""
    sub_index = ""
    
    for i,s in enumerate(array):
        
        if re.search(r'\.{4,}', s):
            if startIndex == -1:
                startIndex = i
            blank_count += 1
        else:
            if blank_count > 0:
                combined_string = ''.join(array[startIndex:startIndex+blank_count])
                combined_string = re.sub(r'(\.{4,}\s*)+', f'[________Enter answer for {question_no}{sub_question}{sub_index}________]', combined_string)
                output_arr.append(combined_string)
            output_arr.append(s)
            blank_count = 0
            startIndex = -1
            
        # Get the current number: e.g 4(a)(ii)
        if s[0] == '(':
            # Add line breaks in front of section markers like (a), (iii), etc
            #s = "<br>" + s
            if re.match(r'^\([a-h]\)', s):
                # For sub questions
                sub_question = s[0:4]
                sub_index = ""
            elif re.match(r'^\([ivx]+\)', s):
                # For sub index like 1(a)(i)
                sub_index = s[0:4]
            print("Number is:", question_no + sub_question + sub_index)
            print("s value is:", s)
            print("Array is:", output_arr)
            print()
    if blank_count > 0:
        combined_string = ''.join(array[startIndex:startIndex+blank_count])
        combined_string = re.sub(r'(\.{4,}\s*)+', f'[________Enter answer for {question_no}{sub_question}{sub_index}________]', combined_string)
        output_arr.append(combined_string)        
        
        
    return output_arr

print(input_arr)
print()
print(merge_blanks(input_arr))