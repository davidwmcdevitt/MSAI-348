import math
import re

class Bayes_Classifier:

    def __init__(self):
        self.positive_reviews= []
        self.negative_reviews= []
        self.review_text = []
        self.unique_words = []
        self.prob_given_positive = []
        self.prob_given_negative = []
        self.review_text = []
        self.positive_reviews = []
        self.negative_reviews = []
        self.ratings = []
        self.id_num = []
        self.positive_words = []
        self.negative_words = []
    
    
    def load_data():
        global data
        f = open('alldata.txt', "r")
        data = f.readlines()
        f.close()
    
    def clean_text(self,text):
        text = text.replace('\n', ' ')
        text = re.sub(r'[^\w\s]', '', text)
        text = text.lower()
        text = text.replace('not ', 'not-')
        text = text.replace('isnt ', 'isnt-')
        text = text.replace(' no ', ' no-')
        stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "youre", "youve", "youll", "youd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "shes", 'her', 'hers', 'herself', 'it', "its", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "thatll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "shouldve", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "arent", 'couldn', "couldnt", 'didn', "didnt", 'doesn', "doesnt", 'hadn', "hadnt", 'hasn', "hasnt", 'haven', "havent", 'isn', "isnt", 'ma', 'mightn', "mightnt", 'mustn', "mustnt", 'needn', "neednt", 'shan', "shant", 'shouldn', "shouldnt", 'wasn', "wasnt", 'weren', "werent", 'won', "wont", 'wouldn', "wouldnt"]
        for i in stopwords:
            s =  " "+i+" "
            text = text.replace(s,' ')
        suffixes = ['ing ','ed ','er ','ers ','s ']
        for s in suffixes:
            text = text.replace(s,' ')
        return text
    
    
    def parse_reviews(self, lines):
        for i in range(len(lines)):
            review = lines[i]
            text = self.clean_text(review.split('|')[2])
            self.ratings.append(review.split('|')[0])
            self.id_num.append(review.split('|')[1])
            
            self.review_text.append(text)
            if review.split('|')[0] == '5':
                self.positive_reviews.append(text)
            if review.split('|')[0] == '1':
                self.negative_reviews.append(text)
        
        
        return self.ratings, self.id_num, self.positive_reviews, self.negative_reviews, self.review_text

    def train(self, lines):
        
        ratings, id_num, positive_reviews, negative_reviews, review_text = self.parse_reviews(lines)
        
        #unique_words = []
        #positive_words = []
        #negative_words = []
    
        for i in range(len(review_text)):
            for g in range(len(review_text[i].split(" "))):
                self.unique_words.append(review_text[i].split(" ")[g])
                
        for i in range(len(positive_reviews)):
            for g in range(len(positive_reviews[i].split(" "))):
                self.positive_words.append(self.positive_reviews[i].split(" ")[g])
                 
        for i in range(len(negative_reviews)):
            for g in range(len(negative_reviews[i].split(" "))):
                self.negative_words.append(self.negative_reviews[i].split(" ")[g])
                
        self.unique_words = list(set(self.unique_words))
        
        #prob_given_positive = []
        #prob_given_negative = []
        
        for i in self.unique_words:
            self.prob_given_positive.append(math.log10((1 + self.positive_words.count(i) / (self.positive_words.count(i) + self.negative_words.count(i)))))
            self.prob_given_negative.append(math.log10((1 + self.negative_words.count(i) / (self.positive_words.count(i) + self.negative_words.count(i)))))
            
        
        return self.prob_given_positive, self.prob_given_negative


    def classify(self, lines):
        ratings = []
        id_num = []
        review_text = []
        predictions = []
        
        for i in range(len(lines)):
            review = lines[i]
            text = self.clean_text(review.split('|')[2])
            ratings.append(review.split('|')[0])
            id_num.append(review.split('|')[1])
            
            #prob_positive = math.log10((1+len(self.positive_reviews))/len(self.review_text))
            #prob_negative = math.log10((1+len(self.negative_reviews))/len(self.review_text))
            
            prob_positive = 0
            prob_negative = 0
            
            words = text.split(' ')
            for word in words:
                if word in self.unique_words:
                    index = self.unique_words.index(word)
                    if self.prob_given_positive[index] + self.prob_given_negative[index] >=1000/len(self.unique_words):
                        prob_positive += self.prob_given_positive[index]
                        prob_negative += self.prob_given_negative[index]
            #print(prob_positive,prob_negative)
            if prob_positive >= prob_negative:
                pred = '5'
                predictions.append('5')
            if prob_negative >prob_positive:
                predictions.append('1')
                pred = '5'
                
            
        
        return predictions

