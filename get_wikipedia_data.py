import wikipedia as wiki
import util

def get_word_count_train_validation():
    d_word_count_t_q = util.get_d_word_count_train_question()
    d_word_count_t_c = util.get_d_word_count_train_choice()
    d_word_count_v_q = util.get_d_word_count_validation_question()
    d_word_count_v_c = util.get_d_word_count_validation_choice()
    d_word_count = {}
    for word in d_word_count_t_q.keys():
        d_word_count.setdefault(word, 0)
        d_word_count[word] += d_word_count_t_q[word]
    for word in d_word_count_t_c.keys():
        d_word_count.setdefault(word, 0)
        d_word_count[word] += d_word_count_t_c[word]
    for word in d_word_count_v_q.keys():
        d_word_count.setdefault(word, 0)
        d_word_count[word] += d_word_count_v_q[word]
    for word in d_word_count_v_c.keys():
        d_word_count.setdefault(word, 0)
        d_word_count[word] += d_word_count_v_c[word]
    return d_word_count
    '''
    sort = sorted(d_word_count.iteritems(), key = lambda dd : dd[1])
    for s in sort:
        print "%s\t%d" % (s[0], s[1])
    '''

def get_wikipedia_content_based_on_word_count_train_validation(d_word_count):
    file = open('data/wikipedia_content_v1.txt', 'w')
    n_word = len(d_word_count.keys())
    n_current = 0
    for word in d_word_count.keys():
        n_current += 1
        print word, n_current, n_word, n_current * 1.0 / n_word
        if not word:
            continue
        lst_title = wiki.search(word)
        if len(lst_title) >= 1:
            for title in lst_title:
                title = title.encode('ascii', 'ignore')
                print 'title', title
                try:
                    content = wiki.page(title).content.encode('ascii', 'ignore')
                except wiki.exceptions.DisambiguationError as e:
                    print 'DisambiguationError', word
                    '''
                    for title_disambiguation in e.options:
                        title_disambiguation = title_disambiguation.encode('ascii', 'ignore')
                        print 'title_disambiguation', title_disambiguation
                        try:
                            content = wiki.page(title_disambiguation).content.encode('ascii', 'ignore')
                        except:
                            pass
                    '''
                except:
                    pass
                for line in content.split('\n'):
                    line = ' '.join(map(util.norm_word, line.split()))
                    if line:
                        file.write(line + '\n')
    file.close()

def get_wikipedia_content_ck12_keyword():
    path_keyword = 'data/ck12_list_keyword.txt'
    lst_keyword = open(path_keyword).readlines()
    n_total = len(lst_keyword)
    file = open('data/wikipedia_sci.txt', 'w')
    for index, line in enumerate(lst_keyword):
        keyword = line.strip('\n').lower()
        print index, n_total, index * 1.0 / n_total, keyword
        try:
            content = wiki.page(keyword).content.encode('ascii', 'ignore')
        except wiki.exceptions.DisambiguationError as e:
            print 'DisambiguationError', keyword
        except:
            print 'Error', keyword
        if not content:
            continue
        for line in content.split('\n'):
            line = ' '.join(map(util.norm_word, line.split()))
            if line:
                file.write(line + '\n')
    file.close()

def get_wikipedia_content_ck12_one_file_per_keyword(ck12_keywords, wiki_dir):
    path_keyword = ck12_keywords
    lst_keyword = open(path_keyword).readlines()
    n_total = len(lst_keyword)
    for index, line in enumerate(lst_keyword):
        keyword = line.strip('\n').lower()
        print index, n_total, index * 1.0 / n_total, keyword
        try:
            content = wiki.page(keyword).content.encode('ascii', 'ignore')
        except wiki.exceptions.DisambiguationError as e:
            print 'DisambiguationError', keyword
        except:
            print 'Error', keyword
        if not content:
            continue
        file = open(wiki_dir + '_'.join(keyword.split()) + '.txt', 'w')
        for line in content.split('\n'):
            line = ' '.join(map(util.norm_word, line.split()))
            if line:
                file.write(line + '\n')
        file.close()

#get_wikipedia_content_ck12_one_file_per_keyword(ck12_keywords, wiki_dir)
#get_wikipedia_content_ck12_keyword()
'''
d = get_word_count_train_validation()
get_wikipedia_content_based_on_word_count_train_validation(d)
'''
