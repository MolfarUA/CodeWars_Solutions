def example_test_cases():
        test.assert_equals(translate("***lo w***d!", ["hello", "world"]), "hello world!")
        test.assert_equals(translate("c**l, w*ak!", ["hell", "cell", "week", "weak"]), "cell, weak!")
        test.assert_equals(translate("hell*, w***d!", ["hello", "hell", "word", "world"]), "hello, world!")
        test.assert_equals(translate("***", ["mel", "dell"]), "mel")
        test.assert_equals(translate("", ["hell", "weak"]), "")
        test.assert_equals(translate("****. ***,", ["aaa", "bbbb"]), "bbbb. aaa,")
        
def translate(s, voc):
    
    s = s.split(' ')
    output = []
    for speech in s:
        for vocabulary in voc:
            
            real_speech = speech_decoder(speech, vocabulary)
        
        if real_speech:
            output.append(real_speech)
            
    return ' '.join(output)

def speech_decoder(speech, vocabulary):
    copy_speech = speech
    length_raw_string = len(copy_speech.translate(str.maketrans('', '', '?!,.')))
    
    if length_raw_string != len(vocabulary):
        return False
    
    i = 0
    output = []
    for word in speech:
        
        if word == '*':
            output.append(vocabulary[i])
            i += 1
            continue
            
        if word in '?!,.':
            output.append(word)
            continue
            
        if word == vocabulary[i]:
            output.append(vocabulary[i])
        else:
            return False
    
        i += 1

    result = ' '.join(output)
    output.clear()
    
    return result
