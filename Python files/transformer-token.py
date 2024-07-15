from transformers import T5Tokenizer, TFT5ForConditionalGeneration

tokenizer = T5Tokenizer.from_pretrained('SJ-Ray/Re-Punctuate')
model = TFT5ForConditionalGeneration.from_pretrained('SJ-Ray/Re-Punctuate')
array = ['Answer  ', 'Description Type of software  Free to download  Code can be modified and redistributed  Subject to copyright legislation  Free software  Freeware  1 mark for each ‘Type of software’ if correct lines are attached to it.', 'Any three from:  Scans files for viruses // detects/identifies a virus Can constantly run in background Can run a scheduled scan Can automatically updating virus definitions Can quarantine a virus Can delete a virus Completes heuristic checking  Notifies user of a possible virus', 'Any three from:  Use a firewall Use of a proxy server Do not use / download software / files from unknown sources  Do not share external storage devices / USB pens Do not open / take care when opening attachments / link Do not connect computer to network / use as stand-alone computer Limiting access to the computer', 'Byte 3 / 10110100', 'Odd parity used Counted / added the number 1’s // Most Bytes have an odd number of 1’s Byte 3 has an even number of 1’s // Byte 3 didn’t follow odd parity', 'Any six from:  Sensor(s) send data/signals to the microprocessor Analogue signal/data from sensor is converted to digital (using ADC) Microprocessor compares data value against set boundaries / pre-set data If value between 21 and 24 « « no action taken If value > 24 °C / signal is sent from microprocessor« « to turn conditioning unit ON//Set to cold If value is < 21 °C signal is sent from microprocessor« « to turn conditioning unit ON//Set to warm Process is repeated for a continuous operation', 'Any two from:  2  Easier / simpler to remember / write down // quicker to transcribe Less likely to make error Less digits to use', '4 marks for 8 correct outputs 3 marks for 6 correct outputs 2 marks for 4 correct outputs 1 mark for 2 correct outputs  A  B  C  X  0  0  0  1  0  0  1  0  0  1  0  1  0  1  1  1  1  0  0  0  1  0  1  1  1  1  0  1  1  1  1  1', '1 mark per gate in correct location', 'Bits are sent using a single wire. Data can be sent or received, but not at the same time.', 'Descriptions', 'Answer  ', 'Description Type of software  Free to download  Code can be modified and redistributed  Subject to copyright legislation  Free software  Freeware  1 mark for each ‘Type of software’ if correct lines are attached to it.', 'Any three from:  Scans files for viruses // detects/identifies a virus Can constantly run in background Can run a scheduled scan Can automatically updating virus definitions Can quarantine a virus Can delete a virus Completes heuristic checking  Notifies user of a possible virus', 'Any three from:  Use a firewall Use of a proxy server Do not use / download software / files from unknown sources  Do not share external storage devices / USB pens Do not open / take care when opening attachments / link Do not connect computer to network / use as stand-alone computer Limiting access to the computer', 'Byte 3 / 10110100', 'Odd parity used Counted / added the number 1’s // Most Bytes have an odd number of 1’s Byte 3 has an even number of 1’s // Byte 3 didn’t follow odd parity', 'Any six from:  Sensor(s) send data/signals to the microprocessor Analogue signal/data from sensor is converted to digital (using ADC) Microprocessor compares data value against set boundaries / pre-set data If value between 21 and 24 « « no action taken If value > 24 °C / signal is sent from microprocessor« « to turn conditioning unit ON//Set to cold If value is < 21 °C signal is sent from microprocessor« « to turn conditioning unit ON//Set to warm Process is repeated for a continuous operation', 'Any two from:  2  Easier / simpler to remember / write down // quicker to transcribe Less likely to make error Less digits to use', '4 marks for 8 correct outputs 3 marks for 6 correct outputs 2 marks for 4 correct outputs 1 mark for 2 correct outputs  A  B  C  X  0  0  0  1  0  0  1  0  0  1  0  1  0  1  1  1  1  0  0  0  1  0  1  1  1  1  0  1  1  1  1  1', '1 mark per gate in correct location', 'Bits are sent using a single wire. Data can be sent or received, but not at the same time.', 'Descriptions', 'Bits are sent using a single wire. Data can be sent or received, but not at the same time.', 'Max 3 – 1 mark for correct answer and 2 marks for correct calculations. Any two from: 16000 × 32  512000 / 1024 Or 16000 × 8   128000 × 32 4096000 / 8 512000 / 1024  Correct answer:  500 kB', '10010', '11110001', 'Any four from:  The program is stored on a secondary storage device Data and instructions are moved to memory / RAM Data and instructions are stored in the same memory / RAM Data and instructions are moved to registers to be executed Instructions are fetched one at a time', 'Smaller file size reduces download / display time // reduces upload time', 'Any four from:  A compression algorithm is used Permanently deleting some data // file cannot be restored to original Colour depth / palette can be reduced Resolution can be reduced // number of pixels can be reduced Less bits will be required for each pixel / colour', 'Quicker to scan « « rather than type into a system  Fewer errors « « no human input', 'Any four from:  Uses a barcode reader / scanner Reader shines light / red laser at barcode White lines reflect (more) light Sensors / photoelectric cells detect light reflected back Different reflections / bars will convert to different binary values', 'Any four from  \x80 (Provides an) interface   \x80 Loads / opens / installs / closes software   \x80 Manages the hardware // manages peripherals // spooling   \x80 Manages the transfer of programs into and out of memory   \x80 Divides processing time // processor management   \x80 Manages file handling   \x80 Manages error handling / interrupts   \x80 Manages security software   \x80 Manages utility software   \x80 Manages user accounts   \x80 Multitasking // Multiprocessing // Multiprogramming // Time slicing   \x80 Batch processing // real time processing']
#input_text = 'the story of this brave brilliant athlete whose very being was questioned so publicly is one that still captures the imagination'
for item in array:
    inputs = tokenizer.encode("punctuate: " + item, return_tensors="tf") 

    result = model.generate(inputs)

    decoded_output = tokenizer.decode(result[0], skip_special_tokens=True)
    print(decoded_output.split('.'))

