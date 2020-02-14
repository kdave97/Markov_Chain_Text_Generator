import random
import nltk
import glob
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
import sys


class MarkovChain:

    def __init__(self):
        
        #self.dirr=auth_dir
        #self.dirr2=auth_dir2
        #self.prob_file1=prob_file1
        #self.prob_file2=prob_file2
        #self.result_file=result_file
        self.choose=0
        self.choose1=0
        #print ("In read")
        #self.read(self.dirr)
        #self.read(self.dirr2)
        

    def read(self,auth_dir):
        print ("Reading Files")
        dirr=auth_dir
        file_list=glob.glob(dirr+"/*.txt")
        print(file_list)
        file = ""
        for f in file_list:
            with open(f,'rb') as infile:
                   file+=infile.read().decode("utf-8")

        file=file.lower()
        tokens=word_tokenize(file)
        tokenize_words=[word for word in tokens if word.isalnum()]
        stop_words=stopwords.words("english")
        
        return self.preprocessing(tokenize_words,stop_words)

    def preprocessing(self,tokenize_words,stop_words):
        print ("Processing! ")
        new_words=[]
        for i in tokenize_words:
            if i not in stop_words:
                new_words.append(i)

        #print (new_words)
        return self.ngrams_generator(new_words)
         
        
    def ngrams_generator(self,new_words):
        bigrams=self.words_to_ngrams(new_words,2,sep=" ")
        #print ("Bigrams: ", bigrams)
        trigrams=self.words_to_ngrams(new_words,3,sep=" ")
        #print ("Trigrams: ", trigrams)
        return self.calculate_probabilities(new_words,bigrams,trigrams)
        

    def words_to_ngrams(self,new_words, n, sep=" "):
        list1=[sep.join(new_words[i:i+n]) for i in range(len(new_words)-n+1)]
        ngrams=[]
        for i in list1:
            ngrams.append(i.split(" "))
        dic={}
        for l in ngrams:
            if tuple(l) in dic:
                dic[tuple(l)] +=1
            else:
                dic[tuple(l)] = 1
        return dict(sorted(dic.items(),key=lambda x:x[1],reverse=True))
    
    def calculate_probabilities(self,new_words,bigrams,trigrams):
        unigram_prob={}
        unigrams={}
        for i in new_words:
            if i not in unigram_prob:
                unigram_prob[i]=new_words.count(i)/len(new_words)
        for i in new_words:
            if i not in unigrams:
                unigrams[i]=1
            else:
                unigrams[i]+=1
        
        bigram_prob={}
        #total=sum(bigrams.values())
        #print ("Total: ",total)
        #for i in bigrams:
        #    if i not in bigram_prob:
        #        bigram_prob[i]=bigrams[i]/total
       

        for i in bigrams:
            if i not in bigram_prob:
                bigram_prob[i]=bigrams[i]/unigrams[i[1]]

        
        
        trigram_prob={}

        #total2=sum(trigrams.values())
        #print (total2)
        #for i in trigrams:
        #    if i not in trigram_prob:
        #        trigram_prob[i]=trigrams[i]/total2
        
     

        for i in trigrams:
            if i not in trigram_prob:
                trigram_prob[i]=trigrams[i]/bigrams[i[1:]]

        
        
        
        
        #print ("\n Unigrams:", unigrams)
        #print ("\n Bigrams:", bigrams)
        #print ("\n Trigrams:", trigrams)
        #print ("\n Unigram: ",unigram_prob)
        #print ("\n Bigram: ",bigram_prob)        
        #print ("\n Trigram: ",trigram_prob)
        
        #self.get_sentence(new_words,unigram_prob,bigram_prob,trigram_prob)
        
        return new_words,unigram_prob,bigram_prob,trigram_prob
    """
    def get_sentence(self,new_words,unigram_prob,bigram_prob,trigram_prob):
        #sentence_list=[]
        sentence_probabilities={}
        for j in range(10):
            probabilities=[]
            sentence_len=20
            sentence=""
            first=random.choice(new_words)
            probabilities.append(unigram_prob[first])
            sentence+=first
            sentence+=" "
            sentence_len-=1
            possible_list={}
            for i in bigram_prob:
                if i[0]==first:
                    possible_list[i]=bigram_prob[i]
            #print (possible_list)
            second=random.choices(list(possible_list.keys()),list(possible_list.values()))[0][1]
            sentence+=second
            sentence+=" "
            sentence_len-=1
            probabilities.append(bigram_prob[(first,second)])

            for words in range(sentence_len):
                trigram_list={}
                for i in trigram_prob:
                    if i[0]==first and i[1]==second:
                        trigram_list[i]=trigram_prob[i]

                #print ("Possible cases: ",trigram_list)
                next_word=random.choices(list(trigram_list.keys()),list(trigram_list.values()))[0][2]
                probabilities.append(trigram_prob[(first,second,next_word)])
                
                sentence+=next_word
                sentence+=" "

                first=second
                second=next_word

            #sentence_list.append(sentence)
            sentence_probabilities[sentence]=probabilities
            #print ("Sentence: ",sentence)
            #print ("Probrability: ",prob)
            #print ("Probability list: ",probabilities)
        
        self.write_file(sentence_probabilities)
    """
    
    def get_sentence(self,unigram_prob,bigram_prob,trigram_prob):
        sentence_list=[]
        for j in range(10):
            sentence_len=20
            sentence=""
            first=random.choices(list(unigram_prob.keys()),list(unigram_prob.values()))[0]
            sentence+=first
            sentence+=" "
            sentence_len-=1
            possible_list={}
            for i in bigram_prob:
                if i[0]==first:
                    possible_list[i]=bigram_prob[i]

            second=random.choices(list(possible_list.keys()),list(possible_list.values()))[0][1]
            sentence+=second
            sentence+=" "
            sentence_len-=1

            for words in range(sentence_len):
                trigram_list={}
                for i in trigram_prob:
                    if i[0]==first and i[1]==second:
                        trigram_list[i]=trigram_prob[i]

                
                next_word=random.choices(list(trigram_list.keys()),list(trigram_list.values()))[0][2]
                
                sentence+=next_word
                sentence+=" "

                first=second
                second=next_word

            sentence_list.append(sentence)
        return sentence_list

    def get_probabilities(self,sentence_list,unigram_prob,bigram_prob,trigram_prob):
        all_prob=[]
        min_prob=0.0001
        for i in sentence_list:
            probabilities=[]
            a=i.split(" ")
            a.pop(-1)
            first=a[0]
            second=a[1]
            if first in unigram_prob:
                probabilities.append(unigram_prob[first])
            else:
                probabilities.append(min_prob)
            if (first,second) in bigram_prob:
                probabilities.append(bigram_prob[(first,second)])
            else:
                probabilities.append(min_prob)

            for j in range(2,len(a)):
                if (a[j-2],a[j-1],a[j]) in trigram_prob:
                    probabilities.append(trigram_prob[(a[j-2],a[j-1],a[j])])
                else:
                    probabilities.append(min_prob)
            all_prob.append(probabilities)

        return all_prob
             



    def write_result(self,result_file,sentence_list):
        with open(result_file,"a") as f:
            f.write("Sentences Generated")
            f.write("\n")
            cnt=1;
            for i in sentence_list:
                print ("\n",file=f)
                print("Sentence "+str(cnt)+":",i,file=f)
                cnt+=1;
            f.close()


    def write_prob1(self,prob_file,prob_list):
        temp=["USING AUTHOR 1 MODEL","PROBABILITIES USING AUTHOR 2 (OTHER) MODEL"]
        with open(prob_file,"a") as f1:
            print (temp[self.choose],file=f1)
            self.choose+=1
            f1.write("Probabilities")
            f1.write("\n")
            cnt=1;
            for i in range(len(prob_list)):
                prob=1
                print ("\n",file=f1)
                print ("Sentence "+str(cnt)+":",prob_list[i],file=f1)
                for k in prob_list[i]:
                    prob*=k
                print ("Total Probability: ",prob,file=f1)
                cnt+=1;
            f1.close()

    def write_prob2(self,prob_file,prob_list):
        temp1=["USING AUTHOR 2 MODEL","PROBABILITIES USING AUTHOR 1 (OTHER) MODEL"]
        with open(prob_file,"a") as f2:
            print (temp1[self.choose1],file=f2)
            f2.write("Probabilities")
            f2.write("\n")
            cnt=1;
            for i in range(len(prob_list)):
                prob=1
                print ("\n",file=f2)
                print ("Sentence "+str(cnt)+":",prob_list[i],file=f2)
                for k in prob_list[i]:
                    prob*=k
                print ("Total Probability: ",prob,file=f2)
                cnt+=1;
            f2.close()
        

        
if __name__=="__main__":

    auth_dir1=sys.argv[1]
    auth_dir2=sys.argv[2]
    prob_file1=sys.argv[3]
    prob_file2=sys.argv[4]
    result_file=sys.argv[5]
    #MarkovChain(auth_dir1,auth_dir2,prob_file1,prob_file2,result_file)
    ## CALLING FOR 1st Author
    q1=MarkovChain()
    words,f1_uni,f1_bi,f1_tri=q1.read(auth_dir1)
    s1_sentences=q1.get_sentence(f1_uni,f1_bi,f1_tri)
    q1.write_result(result_file,s1_sentences)
    s1_prob=q1.get_probabilities(s1_sentences,f1_uni,f1_bi,f1_tri)
    q1.write_prob1(prob_file1,s1_prob)
    ## CALLING for 2nd Author
    q2=MarkovChain()
    words,f2_uni,f2_bi,f2_tri=q2.read(auth_dir2)
    s2_sentences=q2.get_sentence(f2_uni,f2_bi,f2_tri)
    q2.write_result(result_file,s2_sentences)
    s2_prob=q2.get_probabilities(s2_sentences,f2_uni,f2_bi,f2_tri)
    q2.write_prob2(prob_file2,s2_prob)

    #Predicting for 1 Using author 2 unigrams,bigram,trigrams
    s1_s2=q1.get_probabilities(s1_sentences,f2_uni,f2_bi,f2_tri)
    q1.write_prob1(prob_file1,s1_s2)

    s2_s1=q2.get_probabilities(s2_sentences,f1_uni,f1_bi,f1_tri)
    q2.write_prob2(prob_file2,s2_s1)
    print ("Completed!")
