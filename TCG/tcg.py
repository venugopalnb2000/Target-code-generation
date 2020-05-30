import re
import sys

def is_label(s):
	return bool(re.match(r"^L[0-9]*:$", s))


arth = {'+': 'ADD', '*': 'MUL', '-': 'SUB', '/': 'DIV'}
reop = {'==': 'BNE', '!=': 'BE','<': 'BGE', '>': 'BLE', '<=': 'BGT', '>=': 'BLT'}


branch=[]
reg_list=['R0', 'R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'R9', 'R10']
code=[]
used={}
inside_label=0
reg_occ=[]

def gencode(lines):
	global code
	global inside_label
	global branch


	for line in lines:
		tk=line.split()
		
		#If the numbero of tokens is 3 i,e,
		#i = 10
		#a = b
		if(len(tk)==3):
			if(tk[0] not in used.values()):
				if(len(reg_list)==0):
					reg_list.append(reg_occ.pop(0))
				used[reg_list[0]]=tk[0]
				reg_occ.append(reg_list.pop(0))
			# if the token the result variable not present in used dectionary assign a register to it

			#i=0 condition
			#if the the RHS is digit
			if(tk[2].isdigit()):
				#reverse key and value and store in new dict K
				k=dict(map(reversed,used.items()))
				reg=k[tk[0]]

				#Move the value to the register
				c="\tMOV "+reg+" #"+tk[2]

				#append to code list
				code.append(c)

				#Store the register value in the memory
				c="\tSTR "+tk[0]+" "+reg
				code.append(c)

			#if it is a memory location
			else:

				if(tk[2][0]=='&'):
					if(len(reg_list)==0):
						reg_list.append(reg_occ.pop(0))

					k=dict(map(reversed,used.items()))
					reg=k[tk[0]]

					c="\tMOV "+reg+" addr("+tk[2][1:]+")"
					code.append(c)

					# print(used)





				else:

					#If the value RHS is not loaded to register in 'used' dictionary 
					if(tk[2] not in used.values()):
						#get first register from the register list
						if(len(reg_list)==0):
							reg_list.append(reg_occ.pop(0))
						reg=reg_list[0]

						#load the value into the register
						c="\tLDR "+reg+" "+tk[2]
						
						code.append(c)

						#store in the dictionary
						used[reg]=tk[2]

						#pop that register from reg_list
						reg_occ.append(reg_list.pop(0))


					#reversed key-value dict
					k=dict(map(reversed,used.items()))

					#get register
					reg=k[tk[2]]
					# print(reg,line)

					#store instruction 
					if(tk[0][0]!='t'):
						d="\tSTR "+tk[0]+" "+reg

						#append command
						code.append(d)
					reg=k[tk[2]]

					#This block takes into consideration if i = j;j = k;k= l
					# print("HERE",used, line)

					# reg=k[tk[0]]
					# used.pop(reg)
					if(tk[0] in used.values()):
						c="\tMOV "+k[tk[0]]+" "+reg
						code.append(c)
					# reg_list.append(reg)
					# # reg_list.insert(0,reg)
					# reg_occ.remove(reg)
					# reg=k[tk[2]]
					# used[reg]=tk[0]

					#If there is a branch the calculated register is moved to original register
					# print(used,tk[0],line)
					# if(inside_label and tk[0] in used.values()):
					# 	# print("HERE")
					# 	# print("PRESENT ")

					# 	c="\tMOV "+k[tk[0]]+" "+reg

					# 	# k=dict(map(reversed,used.items()))
					# 	code.append(c)
					# 	# inside_label=0


		# number of tokens 5 
		# a = b + c
		# a = b + 10
		elif(len(tk)==5):
			
			# print(used)
			#if 1st operand is not digit
			if(not tk[2].isdigit()):
				#if the operand is not loaded in register
				if(tk[2] not in used.values()):
					if(len(reg_list)==0):
						reg_list.append(reg_occ.pop(0))
					reg=reg_list[0]
					#load the value into the register
					c="\tLDR "+reg+" "+tk[2]
					code.append(c)
					#store in the dictionary
					used[reg]=tk[2]
					#pop that register from reg_list
					reg_occ.append(reg_list.pop(0))

			#if 2nd operand is not digit
			if(not tk[4].isdigit()):
				#if the operand is not loaded in register
				if(tk[4] not in used.values()):
					if(len(reg_list)==0):
						reg_list.append(reg_occ.pop(0))
					reg=reg_list[0]
					#load the value into the register
					c="\tLDR "+reg+" "+tk[4]
					code.append(c)
					#store in the dictionary
					used[reg]=tk[4]
					#pop that register from reg_list
					reg_occ.append(reg_list.pop(0))


			#Arthmetic operation
			if(tk[3] in arth):
				# print("HERE",line)
				# print(used,line,reg_list)

				if(tk[0] not in used.values()):
					if(len(reg_list)==0):
						reg_list.append(reg_occ.pop(0))
					# print("HERE",used)
					used[reg_list[0]]=tk[0]
					# print("HERE",used)

					reg_occ.append(reg_list.pop(0))

				# print(used,line,reg_list)
				#check the 2nd operand is digit
				if(tk[4].isdigit()):
					r2="#"+tk[4]
				else:
					if(tk[4] not in used.values()):
						if(len(reg_list)==0):
							reg_list.append(reg_occ.pop(0))
							# print("HERE",used)
							used[reg_list[0]]=tk[4]
							# print("HERE",used)

							reg_occ.append(reg_list.pop(0))
					k=dict(map(reversed,used.items()))
					r2=k[tk[4]]

				#check the ist operand is digit
				if(tk[2].isdigit()):
					r1="#"+tk[2]
				else:
					# print(tk[2])
					if(tk[2] not in used.values()):
						if(len(reg_list)==0):
							reg_list.append(reg_occ.pop(0))
							# print("HERE",used)
							used[reg_list[0]]=tk[2]
							# print("HERE",used)

							reg_occ.append(reg_list.pop(0))
						# c="\tLDR "
					# print(used)
					k=dict(map(reversed,used.items()))
					# print(k)
					r1=k[tk[2]]
					# print("HERE",r1)


				# print("here",r1)
				k=dict(map(reversed,used.items()))
				r3=k[tk[0]]

				#add sub div mul command
				c="\t"+arth[tk[3]]+" "+r3+" "+r1+" "+r2
				code.append(c)

			#if the result is temperory(t0, t1, ...) we don't store in memery of those
			# only variables like a in a=b+c is stored
			if(str(tk[0][0]) !="t" ):
				# print("herhe",tk[0])
				if(tk[0] in used.values()):
					k=dict(map(reversed,used.items()))
					reg=k[tk[0]]
					# print("reg present ",reg,line )
				else:
					if(len(reg_list)==0):
						reg_list.append(reg_occ.pop(0))
					reg=reg_list.pop(0)
					# print(reg)
					reg_occ.append(reg)
					used[reg]=tk[0]
				# print(reg)
				c="\tSTR "+tk[0]+" "+reg
				code.append(c)
				# print("HERE")
			# print(c)

			#For relational operators
			if(tk[3] in reop):
				# print("hi")

				k=dict(map(reversed,used.items()))
				# print(k)
				r1=k[tk[2]]
				# print(r1)
				if(tk[4].isdigit()):
					r2="#"+tk[4]
				else:
					r2=k[tk[4]]
				c="\tCMP "+r1+" "+r2


				branch.append(reop[tk[3]])
				code.append(c)

		#Branch ifFalse
		elif(tk[0]=="ifFalse"):
			try:
				c="\t"+branch[-1]+" "+tk[-1]
				code.append(c)
			except:
				print("ERROR")

		elif(tk[0]=="goto"):
			c="\tB "+tk[1]
			code.append(c)
		

		elif(is_label(line)):
			inside_label=1
			code.append(line)

		# print("#######################################################")
		# print(line)
		# for i in code:
		# 	print(i)
		# print(used,line)
		# print("#######################################################")




def main():
	if(len(sys.argv)!=2):
		print("File argument  missing.....")
		sys.exit(0)
	try:
		file=sys.argv[1];
		f=open(file,"r");
		lines=[i.strip() for i in f.read().splitlines()]
		# print(lines)
		# print(lines[0].split())
		gencode(lines)
		global code
		global reg_list
		global used
		# print(reg_list)
		k=0
		for i in code:
			print(i)
			k+=1
		# print(used)
		# print(reg_list)
		# print(reg_occ)
		# print(branch)


	except Exception as e:
		print(e)

if __name__ == '__main__':
	main()