from wordexpansion import ChineseSoPmi

sopmier = ChineseSoPmi(inputtext_file='test_corpus.txt',
                       seedword_txtfile='test_seed_words.txt',
                       pos_candi_txt_file='pos_candi.txt',
                       neg_candi_txtfile='neg_candi.txt')
sopmier.sopmi()