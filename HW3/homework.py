#imports
import re, collections

#class with all helper methods
class Helper:
	#useful while converting infix to prefix, and then to differentiate between predicate and operator brackets
	def replace_brackets(self, s, c1, c2):
		new_str=""
		for i in range(0,len(s)):
			if (s[i]=='(' and (i-1)<0) or (s[i]=='(' and not s[i-1].isalnum()):
				new_str+=c1
			elif (s[i]==')' and (i+1)==len(s) and not s[i-1].isalnum()) or (s[i]==')' and not s[i-1].isalnum()):
				new_str+=c2
			else:
				new_str+=s[i]
		return new_str

	#used while converting infix to prefix
	#adds spaces before and after all operators so we can tokenize by space
	def replace_sentence(self,s):
		s=s.replace(' ','')
		s=s.replace('=>','>')
		s=self.replace_brackets(s,'{','}')
		s=s.replace('{',' { ')
		s=s.replace('}',' } ')
		s=s.replace('>',' > ')
		s=s.replace('&',' & ')
		s=s.replace('|',' | ')
		s=s.replace('~',' ~ ')
		s=s.split()
		s=s[::-1]
		for i in range(0,len(s)):
			if s[i]=='{':
				s[i]='}'
			elif s[i]=='}':
				s[i]='{'
		return s

	def get_predicate(self, atom):
		v=atom.split('(',1)
		v=v[0]
		if v[0]=='~':
			v=v[1:]
		return v

	def variable(self, s):
		if s[0].islower():
			return True
		return False

	def constant(self, s):
		if s[0].isupper():
			return True
		return False

	def isNegated(self, s):
		if s[0]=='~':
			return True
		return False

	def negate(self, q):
		if q[0]=='~':
			return q[1:]
		return '~'+q

	def arguments(self, s):
		s=s.split('(')[1]
		s=s.split(')')[0]
		return s.split(',')

	def separate_conjuncts(self, line):
		clauses=line.strip().split('&')
		return clauses



#class to convert from infix to prefix and prefix to infix
class FormConvertor:
	
	#takes the input expression as given in the input file and converts it to a prefix list
	def infix_prefix(self, s):
		operators=['{','}','>','|','&','~']
		h=Helper()
		s=h.replace_sentence(s)
		operator_stack, result_stack= [], []
		for token in s:
			if token not in operators:
				result_stack.append(token)
			elif token=='{':
				operator_stack.append(token)
			elif token=='}':
				while operator_stack and operator_stack[-1] != '{':
					result_stack.append(operator_stack.pop())
				operator_stack.pop()
			elif token in operators:
				while operator_stack and operators.index(operator_stack[-1]) > operators.index(token):
					result_stack.append(operator_stack.pop())
				operator_stack.append(token)
		while operator_stack:
			result_stack.append(operator_stack.pop())
		result_stack=result_stack[::-1]
		return result_stack

	#converts the prefix from a token list format to the nested list format
	def make_prefix_format(self,s):
		for i in range(len(s)-1, -1, -1):
			if s[i]=='~':
				p=[s[i],s[i+1]]
				s.insert(i,p)
				s.pop(i+1)
				s.pop(i+1)
			elif s[i]=='>' or s[i]=='&' or s[i]=='|':
				p=[s[i],s[i+1],s[i+2]]
				s.insert(i,p)
				s.pop(i+1)
				s.pop(i+1)
				s.pop(i+1)
		return s

	#converts the CNF back to an infix format
	def cnf_to_infix(self,prefix):
		infix=""
		if prefix[0] in ['>','&','|']:
			if len(prefix) > 1:
				for i in range(1,len(prefix)):
					if isinstance(prefix[i],list) and len(prefix) > 1:
						p='('+self.cnf_to_infix(prefix[i])+')'
						infix+=p
					else:
						infix+=prefix[i]
					infix+=prefix[0]
			else:
				infix+=prefix[0]
				return infix
		elif prefix[0] == '~':
			infix+=prefix[0]+prefix[1]+prefix[0]
		else:
			infix+=prefix[0]
			return infix
		return infix[:len(infix)-1]

#class to convert to cnf
class CnfConvertor:
	# a=>b is equivalent to ~a|b
	# convert from [>,a,b] to [|,[~,a],b]
	def remove_implies(self,s):
		result=[]
		result.append('|')
		result.append(['~',s[1]])
		result.append(s[2])
		return result

	# recursively parse through the given sentence and remove all implications
	def implications(self,s):
		# if the main clause is an implication
		if s[0]=='>' and len(s)==3:
			s=self.remove_implies(s)
		#parse through sublists and remove all implications inside, recursively
		for i in range(1,len(s)):
			if len(s[i]) > 1 and isinstance(s[i],list):
				s[i]=self.implications(s[i])
		# if the main clause is an implication due to some operations inside then remove implication one last time
		if s[0]=='>' and len(s)==3:
			s=self.remove_implies(s)
		return s

	#propagate the NOT operators inside, also use DeMorgans laws to simplify
	def push_nots(self, s):
		# s[0] will be '~' so propagate its effect to the inner lists
		result=[]
		# if main operator is negation then return atom
		if s[1][0]=='|':
			result.append('&')
		elif s[1][0]=='&':
			result.append('|')
		#if the main operator is negation itself, return the atomic clause as ~(~A)==A
		elif s[1][0]=='~':
			return s[1][1]
		# now check effect of NOT on inner lists
		for i in range(1,len(s[1])):
			if len(s[1][i]) != 1 and isinstance(s[1][i],list):
				result.append(self.push_nots(['~',s[1][i]]))
			else:
				result.append(['~',s[1][i]])
		return result

	# recursively push all negations to inner terms
	def handle_negations(self,s):
		if s[0] == '~' and len(s) ==2 and isinstance(s[1], list) and len(s[1]) != 1:
			s=self.push_nots(s)
		#recursively handle nested lists
		for i in range(1,len(s)):
			if len(s[i]) > 1 and isinstance(s[i], list):
				s[i]=self.handle_negations(s[i])
		if s[0] == '~' and len(s) ==2 and isinstance(s[1], list) and len(s[1]) != 1:
			s=self.push_nots(s)
		return s

	#check if given statements can be OR-distributed
	def check_dist(self, s):
		if s[0]=='|':
			for i in range(1, len(s)):
				if len(s[i]) > 1 and isinstance(s[i], list):
					if s[i][0] == '&':
						return True
		return False

	#recursively distribute ORs inside
	def do_dist(self, s):
		if self.check_dist(s):
			s=self.or_dist(s)
		#handle nested lists
		for i in range(1,len(s)):
			if len(s[i]) > 1 and isinstance(s[i],list):
				s[i]=self.do_dist(s[i])
		if self.check_dist(s):
			s=self.or_dist(s)
		return self.simple(s)

	#distribute ORs in an atomic sentence
	def or_dist(self, s):
		result=[]
		result.append('&')
		if s[1][0]=='&' and s[2][0]=='&':
			result.append(self.do_dist(['|',s[1][1],s[2][1]]))
			result.append(self.do_dist(['|',s[1][1],s[2][2]]))
			result.append(self.do_dist(['|',s[1][2],s[2][1]]))
			result.append(self.do_dist(['|',s[1][2],s[2][2]]))
		else:
			if s[1][0]=='&':
				if len(s[2])>2 and isinstance(s[2],list):
					if self.check_dist(s[2]):
						s[2]=self.do_dist(s[2])
						result.append(self.do_dist(['|',s[1][1],s[2][1]]))
						result.append(self.do_dist(['|',s[1][1],s[2][2]]))
						result.append(self.do_dist(['|',s[1][2],s[2][1]]))
						result.append(self.do_dist(['|',s[1][2],s[2][2]]))
					else:
						result.append(self.do_dist(['|',s[1][1],s[2]]))
						result.append(self.do_dist(['|',s[1][2],s[2]]))
				else:
					result.append(self.do_dist(['|',s[1][1],s[2]]))
					result.append(self.do_dist(['|',s[1][2],s[2]]))
			else:
				#yoooooooo
				if len(s[1])>2 and isinstance(s[1],list):
					if self.check_dist(s[1]):
						s[1]=self.do_dist(s[1])
						result.append(self.do_dist(['|',s[1][1],s[2][1]]))
						result.append(self.do_dist(['|',s[1][1],s[2][2]]))
						result.append(self.do_dist(['|',s[1][2],s[2][1]]))
						result.append(self.do_dist(['|',s[1][2],s[2][2]]))
					else:
						result.append(self.do_dist(['|',s[1],s[2][1]]))
						result.append(self.do_dist(['|',s[1],s[2][2]]))
				else:
					result.append(self.do_dist(['|',s[1],s[2][1]]))
					result.append(self.do_dist(['|',s[1],s[2][2]]))
		return self.simple(result)

	def make_simple(self, o, l, c):
		result=[]
		result.append(o)
		if isinstance(l, str):
			result.append(l[0])
		else:
			result.append(self.make_simple(o, l[:len(l)-1], l[len(l)-1]))
		result.append(c)
		return result

	def simple(self, s):
		if len(s) > 3 and isinstance(s, list):
			s=self.make_simple(s[0], s[1: len(s)-1], s[len(s)-1])
		for i in range(1, len(s)):
			if len(s[i]) > 1 and isinstance(s[i], list):
				s[i]=self.simple(s[i])
		if len(s) > 3 and isinstance(s, list):
			s=self.make_simple(s[0], s[1: len(s)-1], s[len(s)-1])
		return s

	def already(self, r, s):
		for i in range(1, len(r)):
			if r[i] == s:
				return True
		return False

	def duplicates(self, s):
		if len(s) > 2 and isinstance(s, list):
			result=[s[0], s[1]]
			for i in range(2, len(s)):
				if not self.already(result, s[i]):
					result.append(s[i])
			if len(result) == 2 and isinstance(result, list):
				return result[1]
			return result
		else:
			return s

	def remove_duplicates(self, s):
		if isinstance(s, str):
			return s
		s=self.duplicates(s)
		for i in range(1, len(s)):
			if len(s[i]) > 1 and isinstance(s[i], list):
				s[i]= self.remove_duplicates(s[i])
		s=self.duplicates(s)
		return s

	def clean_sentence(self, s):
		result=[]
		#this is because a negation is treated as a separate literal
		if s[0]=='~':
			return s
		result.append(s[0])
		main_operator=s[0]
		#this is going to convert (and, (and, a, b), c) to (and, a, b, c)
		for i in range(1, len(s)):
			if s[i][0]==main_operator:
				for j in range(1, len(s[i])):
					result.append(s[i][j])
			else:
				result.append(s[i])
		return result

	def cleaning(self, s):
		if isinstance(s,str):
			return s
		s=self.clean_sentence(s)
		for i in range(1,len(s)):
			if len(s[i])>1 and isinstance(s[i],list):
				s[i]=self.cleaning(s[i])
		s=self.clean_sentence(s)
		return s

	def convert_cnf(self, s):
		result=[]
		if len(s)==0:
			return s
		elif len(s)==1:
			return s[0]
		else:
			result=self.implications(s)
			result=self.handle_negations(result)
			result=self.simple(result)
			result=self.do_dist(result)
			result=self.cleaning(result)
			result=self.duplicates(result)
			return result


#class to build KB and standardize
class KBOperations:
	
	def make_kb(self, kb, line):
		h=Helper()
		dic={}
		disj=line.split('|')
		for item in disj:
			pred=h.get_predicate(item)
			if pred in dic:
				dic[pred].append(item)
			else:
				dic[pred]=[item]
		kb.append(dic)
		return kb

	def standardize_kb(self, kb):
		h=Helper()
		new_kb, already= [], {}
		for item in kb:
			d, here= {}, []
			for key in item:
				x=item[key]
				nl=[]
				for atom in x:
					pred=h.get_predicate(atom)
					if atom[0]=='~':
						pred='~'+pred
					pred+='('
					args=h.arguments(atom)
					for i in args:
						if h.variable(i):
							if i not in here:
								here.append(i)
								if i in already:
									n=already[i]
									already[i]=n+1
									pred+=i+str(n+1)+','
								elif i not in already:
									pred+=i+'1,'
									already[i]=1
							elif i in here:
								n=already[i]
								pred+=i+str(n)+','
						else:
							pred+=i+','
					pred=pred[:len(pred)-1]+')'
					nl.append(pred)
				p=h.get_predicate(atom)
				d[p]=nl
			new_kb.append(d)
		return new_kb

#class for resolution
class LogicEngine:
	def __init__(self):
		self.h=Helper()

	def check_unify(self, s1, s2):
		s, a1, a2, bound= [], self.h.arguments(s1), self.h.arguments(s2), {}
		if len(a1)==len(a2):
			i=0
			while i < len(a1):
				if self.h.constant(a1[i]) and self.h.constant(a2[i]):
					if a1[i]==a2[i]:
						s.append(a1[i])
					else:
						break
				elif self.h.constant(a1[i]) and a2[i] not in bound:
					s.append(a1[i])
					bound[a2[i]]=a1[i]
				elif a2[i] in bound:
					if bound[a2[i]] != a1[i]:
						break
					else:
						a.append(a1[i])
				else:
					if self.h.variable(a2[i]) and a2[i] not in bound:
						s.append(a1[i])
						bound[a2[i]]=a1[i]
					elif a2[i] in bound:
						if bound[a2[i]] != a1[i]:
							break
						else:
							s.append(a1[i])
					else:
						s.append(a1[i])
				i+=1
			if i < len(a1):
				return None
		else:
			return None
		return s

	def unify(self, sub, i):
		br=self.h.get_predicate(i)
		if i[0]=='~':
			br='~'+br
		br+='('
		s=self.h.arguments(i)
		for item in s:
			if item in sub:
				br+=sub[item]+','
			else:
				br+=item+','
		br=br[:len(br)-1]+')'
		return br

	def resolve(self, query, kb):
		key=self.h.get_predicate(query)
		for i in range(0,len(kb)):
			hs=kb[i]
			index=0
			if key in hs:
				g=hs[key]
				isneg=self.h.isNegated(query)
				if isneg:
					j=0
					while j<len(g):
						t=g[j]
						if t[0]!='~':
							y=self.check_unify(query,t)
							if y:
								r=self.h.arguments(t)
								sub={}
								k=0
								while k<len(r):
									sub[r[k]]=y[k]
									k+=1
								index=j
								statement=[]
								for k in hs:
									if k != key:
										temp=hs[k]
										for ti in temp:
											statement.append(self.unify(sub,ti))
								p=0
								while p<len(g):
									if p != index:
										statement.append(self.unify(sub,g[p]))
									p+=1
								if len(statement)==0:
									return True
								new_kb=kb[:]
								new_kb.pop(i)
								q=0
								while q<len(statement):
									ans=self.resolve(statement[q],new_kb)
									if not ans:
										break
									q+=1
								if q==len(statement):
									return True
						j+=1
				else:
					j=0
					while j<len(g):
						t=g[j]
						if t[0]=='~':
							y=self.check_unify(query,t)
							if y:
								r=self.h.arguments(t)
								sub={}
								k=0
								while k<len(r):
									sub[r[k]]=y[k]
									k+=1
								index=j
								statement=[]
								for k in hs:
									if k != key:
										temp=hs[k]
										for ti in temp:
											statement.append(self.unify(sub,ti))
								p=0
								while p<len(g):
									if p != index:
										statement.append(self.unify(sub,g[p]))
									p+=1
								if len(statement)==0:
									return True
								new_kb=kb[:]
								new_kb.pop(i)
								q=0
								while q<len(statement):
									ans=self.resolve(statement[q],new_kb)
									if not ans:
										break
									q+=1
								if q==len(statement):
									return True
						j+=1
		return False

def main():
	inp='input.txt'
	out='output.txt'
	cnfs=[]
	with open(inp) as f:
		outputfilename = open(out, "w")
		queries=[]
		number_of_queries=int(f.readline().strip())
		for i in range(0, number_of_queries):
			queries.append(f.readline().strip().replace(' ',''))
		number_of_sentences = int(f.readline().strip())
		for i in range(0,number_of_sentences):
			line=f.readline().strip()
			fc=FormConvertor()
			c=CnfConvertor()
			h=Helper()
			line=fc.infix_prefix(line)
			line=fc.make_prefix_format(line)
			if not isinstance(line,list):
				cnf_in=line
			else:
				line=line[0]
				cnf = c.convert_cnf(line)
				if isinstance(cnf,str):
					cnf_in=cnf
				else: 
					cnf_in=fc.cnf_to_infix(cnf)
			cnf_in=h.replace_brackets(cnf_in,'','')
			cnfs.append(cnf_in)
	
	clause_list=[]
	for x in cnfs:
		c=h.separate_conjuncts(x)
		for item in c:
			clause_list.append(item)
	k=KBOperations()
	kb=[]
	for item in clause_list:
		kb=k.make_kb(kb, item)
	kb=k.standardize_kb(kb)
	le=LogicEngine()
	r=[]
	for item in queries:
		item=h.negate(item)
		kb=k.make_kb(kb, item)
		ans=le.resolve(item,kb)
		r.append(ans)
		kb.pop()
	o=open(out,'w')
	for item in r:
		if item==True:
			o.write('TRUE\n')
		else:
			o.write('FALSE\n')
	o.close()

if __name__=='__main__':
	main()