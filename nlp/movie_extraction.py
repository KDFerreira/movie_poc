#!/usr/bin/env python
#import numpy
from movie import Movie

#import nltk

import _mysql

import datetime

import time

#def addTags(raw_data):
#    raw_data = nltk.word_tokenize(raw_data)
#    raw_data = nltk.pos_tag(raw_data)
#    return raw_data

def sql_get_titles(database_name, table, column):

    titles = []

    connector = _mysql.connect("MIEmovie.db.10555713.hostedresource.com","MIEmovie","Summer#2014","MIEmovie")

    connector.query("SELECT " + column + " FROM " + table)

    results = connector.store_result()

    title = results.fetch_row()

    while title != ():

        titles.append(title[0][0])

        title = results.fetch_row()

    return titles



def title(sentence, movie):

    for title in sql_get_titles('movieGW', 'moviesintheatres', 'title'):

        if title.lower() in sentence:

            movie.set_title(title)

    for title in sql_get_titles('movieGW', 'opening_movies', 'title'):

        if title.lower() in sentence:

            movie.set_title(title)

    for title in sql_get_titles('movieGW', 'upcomingmovies', 'title'):

        if title.lower() in sentence:

            movie.set_title(title)



def parental_rating(sentence, movie):

    tokened = sentence.split(' ')

    for word in tokened:

        if word in open("movie/pg.txt").read().split('\n'):

            movie.set_parental_rating("PG")

        elif word in open("movie/pg-13.txt").read().split('\n'):

            movie.set_parental_rating("PG-13")

        elif word in open("movie/r.txt").read().split('\n'):

            movie.set_parental_rating("R")            



def genre(sentence, movie):

    genre_list = []

    genres = open("movie/genre.txt").read().split('\n')

    for genre in genres:

        if genre in sentence:

            genre_list.append(genre)

    movie.set_genre(genre_list)



def directors(sentence, movie):

    if "directed by" in sentence:

        index = sentence.index("directed by")

        sentence = sentence[index + 12:]

        name_length = 0

        sentence = sentence.replace(',', ' _').split(' ')

        temp = []



        for item in sentence:

            if name_length < 3:

                temp.append(item)

                name_length += 1

                if item == "and" or item == "or" or item == '_':

                    name_length = 0

        sentence = temp



        i = 0

        j = 0

        while i < len(sentence):

            if sentence[i] == "or":

                while j < i:

                    if sentence[j] == '_':

                        sentence[j] = "or"

                    j += 1

            elif sentence[i] == "and":

                while j < i:

                    if sentence[j] == '_':

                        sentence[j] = "and"

                    j += 1

            i += 1



        temp = []

        phrase = ''

        for item in sentence:

            if item == "and":

                temp.append(phrase.strip())

                temp.append("and")

                phrase = ''

            elif item == "or":

                temp.append(phrase.strip())

                temp.append("or")

                phrase = ''

            else:

                phrase += item + ' '

        temp.append(phrase.strip())

        sentence = temp

        movie.set_directors(sentence)



def stars(sentence, movie):

    if "starring" in sentence:

        index = sentence.index("starring")

        sentence = sentence[index + 9:]

        name_length = 0

        sentence = sentence.replace(',', ' _').split(' ')

        temp = []



        for item in sentence:

            if name_length < 3:

                temp.append(item)

                name_length += 1

                if item == "and" or item == "or" or item == '_':

                    name_length = 0

        sentence = temp



        i = 0

        j = 0

        while i < len(sentence):

            if sentence[i] == "or":

                while j < i:

                    if sentence[j] == '_':

                        sentence[j] = "or"

                    j += 1

            elif sentence[i] == "and":

                while j < i:

                    if sentence[j] == '_':

                        sentence[j] = "and"

                    j += 1

            i += 1



        temp = []

        phrase = ''

        for item in sentence:

            if item == "and":

                temp.append(phrase.strip())

                temp.append("and")

                phrase = ''

            elif item == "or":

                temp.append(phrase.strip())

                temp.append("or")

                phrase = ''

            else:

                phrase += item + ' '

        temp.append(phrase.strip())

        sentence = temp

        movie.set_stars(sentence)



    elif "with" in sentence:

        index = sentence.index("with")

        sentence = sentence[index + 5:]

        name_length = 0

        sentence = sentence.replace(',', ' _').split(' ')

        temp = []



        for item in sentence:

            if name_length < 3:

                temp.append(item)

                name_length += 1

                if item == "and" or item == "or" or item == '_':

                    name_length = 0

        sentence = temp



        i = 0

        j = 0

        while i < len(sentence):

            if sentence[i] == "or":

                while j < i:

                    if sentence[j] == '_':

                        sentence[j] = "or"

                    j += 1

            elif sentence[i] == "and":

                while j < i:

                    if sentence[j] == '_':

                        sentence[j] = "and"

                    j += 1

            i += 1

        temp = []

        phrase = ''

        for item in sentence:

            if item == "and":

                temp.append(phrase.strip())

                temp.append("and")

                phrase = ''

            elif item == "or":

                temp.append(phrase.strip())

                temp.append("or")

                phrase = ''

            else:

                phrase += item + ' '

        temp.append(phrase.strip())

        sentence = temp

        movie.set_stars(sentence)



def release_interval(sentence, movie):

    #One week = 604800.0

    #One day = 86400.0

    if "new this month" in sentence:

        if int(datetime.date.today().strftime("%m")) in [1, 3, 5, 7, 8, 10, 12]:

            movie.set_release_interval((int(time.mktime(datetime.date.today().timetuple())) - int(datetime.date.today().strftime("%d")) * 86400, int(time.mktime(datetime.date.today().timetuple())) + (31 - int(datetime.date.today().strftime("%d"))) * 86400))

        elif int(datetime.date.today().strftime("%m")) in [4, 6, 9, 11]:

            movie.set_release_interval((int(time.mktime(datetime.date.today().timetuple())) - int(datetime.date.today().strftime("%d")) * 86400, int(time.mktime(datetime.date.today().timetuple())) + (30 - int(datetime.date.today().strftime("%d"))) * 86400))

        elif int(datetime.date.today().strftime("%m")) == 2:

            movie.set_release_interval((int(time.mktime(datetime.date.today().timetuple())) - int(datetime.date.today().strftime("%d")) * 86400, int(time.mktime(datetime.date.today().timetuple())) + (28 - int(datetime.date.today().strftime("%d"))) * 86400))

    elif "new" in sentence:

        movie.set_release_interval((int(time.mktime(datetime.date.today().timetuple())) - int(datetime.date.today().strftime("%w")) * 86400, int(time.mktime(datetime.date.today().timetuple())) + (7 - int(datetime.date.today().strftime("%w"))) * 86400))



def keywords(sentence, movie):

    about_index = None

    if "about" in sentence:

        about_index = sentence.index("about")

    if about_index:

        sentence = sentence[about_index + 6:]

   # tagged_sentence = addTags(sentence)

  #  reformed_sentence = ''

  #  for (word, tag) in tagged_sentence:

    #    if tag == 'NNPS' or tag == 'NNS':

       #     if word.endswith('s'):

         #       word = word[:-1]

        #reformed_sentence += word + ' '

    #reformed_sentence = reformed_sentence.strip()

    reformed_sentence = sentence

    name_length = 0

    sentence = reformed_sentence.replace(',', '_').split(' ')

    temp = []



    for item in sentence:

        if name_length < 3:

            temp.append(item)

            name_length += 1

            if item == "and" or item == "or" or item == '_':

                name_length = 0

    sentence = temp

    i = 0

    j = 0

    while i < len(sentence):

        if sentence[i] == "or":

            while j < i:

                if sentence[j] == '_':

                    sentence[j] = "or"

                j += 1

        elif sentence[i] == "and":

            while j < i:

                if sentence[j] == '_':

                    sentence[j] = "and"

                j += 1

        i += 1

    temp = []

    phrase = ''

    for item in sentence:

        if item == "and":

            temp.append(phrase.strip())

            temp.append("and")

            phrase = ''

        elif item == "or":

            temp.append(phrase.strip())

            temp.append("or")

            phrase = ''

        else:

            phrase += item + ' '

    temp.append(phrase.strip())

    sentence = temp

    movie.set_keywords(sentence)



def language(sentence, movie):

    languages = open("movie/languages.txt").read().split('\n')

    for language in languages:

        if language in sentence:

            movie.set_language(language)



def extractTitle(sentence, movie):

    if movie.get_title() != '' and movie.get_title() in sentence:

        if sentence.index(movie.get_title()) > 0 and sentence.index(movie.get_title()) + len(movie.get_title()) <= len(sentence):

            sentence = sentence.replace(' ' + str(movie.get_title()) + ' ', '')

        else:

            sentence = sentence.replace(movie.get_title(), '')

        sentence = sentence.strip()

    return sentence



def movie(sentence):

    movie_list = []

    m = Movie()

    stars(sentence, m)

    sentence = sentence.lower()

    title(sentence, m)

    sentence = extractTitle(sentence, m)

    parental_rating(sentence, m)

    genre(sentence, m)

    directors(sentence, m)

    release_interval(sentence, m)

    keywords(sentence, m)

    language(sentence, m)





    moviesintheatres = []

    opening_movies = []

    upcomingmovies = []

    

    connector = _mysql.connect('MIEmovie.db.10555713.hostedresource.com','MIEmovie','Summer#2014','MIEmovie')

    connector.query("SELECT * FROM moviesintheatres")

    result = connector.store_result()

    mov = result.fetch_row()

    while mov != ():

        moviesintheatres.append(mov[0])

        mov = result.fetch_row()

        

    connector.query("SELECT * FROM opening_movies")

    result = connector.store_result()

    mov = result.fetch_row()

    while mov != ():

        opening_movies.append(mov[0])

        mov = result.fetch_row()

        

    connector.query("SELECT * FROM upcomingmovies")

    result = connector.store_result()

    mov = result.fetch_row()

    while mov != ():

        upcomingmovies.append(mov[0])

        mov = result.fetch_row()



    allmovies = moviesintheatres + opening_movies + upcomingmovies

    for movie in allmovies:

        if movie[1] == m.get_title():

            movie_title = movie[1]



            #parental_rating

            if movie[2] == '':

                movie_parental_rating = "Not available"

            else:

                movie_parental_rating = movie[2]



            #duration

            if movie[3] == '':

                movie_duration = "Not available"

            else:

                movie_duration = movie[3]



            #genre

            if movie[4] == '':

                movie_genre = "Not available"

            else:

                movie_genre = movie[4]



            #rating

            if movie[5] == '':

                movie_rating = '-'

            else:

                movie_rating = movie[5]



            #directors

            if movie[6] == '':

                movie_directors = "Not available"

            else:

                movie_directors = movie[6]



            #writers

            if movie[7] == '':

                movie_writers = "Not available"

            else:

                movie_writers = movie[7]



            #stars

            if movie[8] == '':

                movie_stars = "Not available"

            else:

                movie_stars = movie[8]



            #cast

            if movie[9] == '':

                movie_cast = "Not available"

            else:

                movie_cast = movie[9]



            #language

            if movie[10] == '':

                movie_language = "Not available"

            else:

                movie_language = movie[10]



            #release_date

            if movie[11] == '0' or movie[11] == '':

                movie_release_date = "Not available"

            else:

                movie_release_date = str(datetime.datetime.fromtimestamp(float(movie[11])).strftime('%d-%m-%Y'))



            #keywords

            if movie[12] == '':

                movie_keywords = "Not available"

            else:

                movie_keywords = movie[12]



            return "Title: " + movie_title + "\nParental rating: " + movie_parental_rating + "\nDuration: " + movie_duration + "\nGenre: " + movie_genre + "\nRating: " + movie_rating + "/10" + "\nDirector(s): " + movie_directors + "\nWriter(s): " + movie_writers + "\nStar(s): " + movie_stars + "\nCast: " + movie_cast + "\nRelease date: " + movie_release_date + "\nKeyword(s): " + movie_keywords + "\nLanguage(s): " + movie_language

        else:

            parental_rating_pass = False

            genre_pass = False

            director_pass = False

            stars_pass = False

            release_date_pass = False

            keywords_pass = False

            language_pass = False



            prp = False

            gp = False

            dp = False

            sp = False

            rdp = False

            kp = False

            lp = False



            #parental_rating check

            if m.get_parental_rating() == '':

                parental_rating_pass = True

                prp = True

            elif m.get_parental_rating() == movie[2]:

                parental_rating_pass = True



            #genre check

            if m.get_genre() == []:

                genre_pass = True

                gp = True

            else:

                for m_genre in m.get_genre():

                    if m_genre in movie[4].lower():

                        genre_pass = True

                    elif m_genre not in movie[4].lower():

                        genre_pass = False



            #director check

            if m.get_directors() == []:

                director_pass = True

                dp = True

            else:

                i = 1

                if m.get_directors()[i-1].lower() in movie[6].lower():

                    director_pass = True

                while i < len(m.get_directors()):

                    if m.get_directors()[i].lower() == 'and':

                        if m.get_directors()[i-1].lower() in movie[6].lower() and m.get_stars()[i+1].lower() in movie[8].lower():

                            director_pass = True

                        else:

                            director_pass = False

                    elif m.get_directors()[i].lower() == 'or':

                        if m.get_directors()[i-1].lower() in movie[6].lower() or m.get_stars()[i+1].lower() in movie[8].lower():

                            director_pass = True

                        else:

                            director_pass = False

                    i += 2



            #stars check

            if m.get_stars() == []:

                stars_pass = True

                sp = True

            else:

                i = 1

                if m.get_stars()[i-1].lower() in movie[8].lower():

                    stars_pass = True

                while i < len(m.get_stars()):

                    if m.get_stars()[i].lower() == 'and':

                        if m.get_stars()[i-1].lower() in movie[8].lower() and m.get_stars()[i+1].lower() in movie[8].lower():

                            stars_pass = True

                        else:

                            stars_pass = False

                    elif m.get_stars()[i].lower() == 'or':

                        if m.get_stars()[i-1].lower() in movie[8].lower() or m.get_stars()[i+1].lower() in movie[8].lower():

                            stars_pass = True

                        else:

                            stars_pass = False

                    i += 2



            #release_date check

            if m.get_release_interval() == (0, 0):

                release_date_pass = True

                rdp = True

            else:

                if m.get_release_interval()[0] <= int(movie[11]) and int(movie[11]) <= m.get_release_interval()[1]:

                    release_date_pass = True

                    

                else:

                    release_date_pass = False



            #keywords check

            if m.get_keywords() == []:

                keywords_pass = True

                kp = True

            else:

                i = 1

                if m.get_keywords()[i-1].lower() in movie[12].lower():

                    keywords_pass = True

                while i < len(m.get_keywords()):

                    if m.get_keywords()[i].lower() == 'and':

                        if m.get_keywords()[i-1].lower() in movie[12].lower() and m.get_stars()[i+1].lower() in movie[8].lower():

                            keywords_pass = True

                        else:

                            keywords_pass = False

                    elif m.get_keywords()[i].lower() == 'or':

                        if m.get_keywords()[i-1].lower() in movie[12].lower() or m.get_stars()[i+1].lower() in movie[8].lower():

                            keywords_pass = True

                        else:

                            keywords_pass = False

                    i += 2              

            if m.get_language() == '':

                language_pass = True

                lp = True

            else:

                if m.get_language().lower() in movie[10].lower():

                    language_pass = True

                else:

                    language_pass = False     

        if prp and gp and dp and sp and rdp and lp:

            if keywords_pass:

                movie_list.append(movie[1])             

        elif parental_rating_pass and genre_pass and director_pass and stars_pass and release_date_pass and language_pass:

            movie_list.append(movie[1])       

        #print(release_date_pass)

    recommend = ''

    for item in movie_list:

        recommend += '\n' + item

    if recommend == '':

        return "Looks like nothing in our database matches what you are searching for."

    else:

        return "I would recommend: " + recommend


connector = _mysql.connect("MIEmovie.db.10555713.hostedresource.com","MIEmovie","Summer#2014","MIEmovie")
connector.query("SELECT * FROM mentions ORDER BY mention_id DESC LIMIT 1")
results = connector.store_result()
tweet = results.fetch_row()[0][1]
print(movie(tweet))
##print(movie("what's a movie with jonah hill"))
