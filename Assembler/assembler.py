#Om Shri Ganeshaye Namah

symbol_table = {
    "R0": 0,
    "R1": 1,
    "R2": 2,
    "R3": 3,
    "R4": 4,
    "R5": 5,
    "R6": 6,
    "R7": 7,
    "R8": 8,
    "R9": 9,
    "R10": 10,
    "R11": 11,
    "R12": 12,
    "R13": 13,
    "R14": 14,
    "R15": 15,
    "SCREEN": 16384,
    "KBD": 24576,
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,
}
comp ={
    "0":   "0101010",
    "1":   "0111111",
    "-1":  "0111010",
    "D":   "0001100",
    "A":   "0110000",
    "!D":  "0001101",
    "!A":  "0110001",
    "-D":  "0001111",
    "-A":  "0110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "D+A": "0000010",
    "D-A": "0010011",
    "A-D": "0000111",
    "D&A": "0000000",
    "D|A": "0010101",
    "M":   "1110000",
    "!M":  "1110001",
    "-M":  "1110011",
    "M+1": "1110111",
    "M-1": "1110010",
    "D+M": "1000010",
    "D-M": "1010011",
    "M-D": "1000111",
    "D&M": "1000000",
    "D|M": "1010101"
}

dest = {   
    "M":   "001",
    "D":   "010",
    "MD":  "011",
    "A":   "100",
    "AM":  "101",
    "AD":  "110",
    "AMD": "111",
    "":"000"
}

jump = {    
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111",
    "":"000"
}

source_file = input("Enter the file path: ")
output_file = open("output.txt", "w")
source = open(source_file, mode = 'r')
source = source.read().split("\n")
output = []
position = 0
linecount = 0
while(position < len(source)):
    source[position] = source[position].replace(" ", "");
    source[position] = source[position].replace("\t", "");
    if "//" in source[position]:
        source[position]  =  source[position].split('//')[0]
    if (source[position] == ""):
        source.remove(source[position])
        position-=1
    position+=1

for insturction in source:
    if insturction != "" and insturction.startswith("(") and insturction.endswith(")"):
        symbol_table[insturction[1:-1]] = linecount
        source.remove(insturction)
        linecount-=1
    linecount+=1
reg = 0

for instruction in source:
    if instruction[0] == "@":
        if instruction[1:].isdigit():
            output.append(f"{int(instruction[1:]):016b}\n")
        else:
            if(instruction[1:] in symbol_table):
                output.append(f"{int(symbol_table[instruction[1:]]):016b}\n")
            else:
                symbol_table[instruction[1:]] = 16+reg
                reg+=1
                output.append(f"{int(symbol_table[instruction[1:]]):016b}\n")
    else:
        out = "111"
        if "=" in instruction:
            divide = instruction.split("=")
            divide [1] = divide[1].partition(';')
            out += comp[divide[1][0]]+ dest[divide[0]] + jump[divide[1][-1]]+'\n'
            output.append(out)
        else:
            divide = list(instruction.partition('='))
            divide[0] = divide[0].split(";")
            out += comp[divide[0][0]] + dest[divide[-1]]+ jump[divide[0][-1]]+'\n'
            output.append(out)

output_file.writelines(output)
output_file.close()

