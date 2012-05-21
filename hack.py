#!/usr/bin/env python
#-*- coding:utf-8 -*-

import math
import sys
import urllib2, re
from BeautifulSoup import BeautifulSoup as BS

keyString = 'UMh]`ahyY`g`]_^Z``_]'
indexbase = " !\"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~"

def ChkPwd(keyin):
    #print "keyin:", keyin
    enqlen = len(keyString)
    passlen = len(keyin)
    decrypted = ""
    
    if passlen <= 0:
        print "パスワードを入力してください"
        return False
    
    i = 0
    j = passlen - 1
    k = 0
    while i < enqlen:
        if j < 0:
            j = passlen -1
        chr1 = indexbase.index(keyin[j])
        chr2 = indexbase.index(keyString[i])
        #print j, i
        #print keyin[j], keyString[i]
        #print chr1, chr2
        #print "------------"

        if chr2 < (chr1 + j):
            nbase = (chr1 + j - chr2) / 0x5f
            k += int(0x5f * math.ceil(nbase))
            
        k += int(chr2 - chr1 - j)
        decrypted += indexbase[k]
        i += 1
        j -= 1
        k = 0

    decryptedPassword = decrypted[len(decrypted)-passlen:len(decrypted)]
    #print "decrypted:", decrypted
    #print "decryptedPassword = decrypted[%d:%d] = %s" % (len(decrypted)-passlen, len(decrypted), decryptedPassword)
    if keyin == decryptedPassword:
        decryptedPath = decrypted[0:len(decrypted)-passlen]
        passlen = len(decryptedPath)
        targetUrl = ""
        i = 0
        while i < passlen:
            chr1 = decryptedPath[i]
            if chr1 == "%":
                chr2 = decryptedPath[i:i+6]
                targetUrl += chr2
                i += 11
            else:
                targetUrl += chr1
            i += 1
        
        #print "correct!"
        #print "targetUrl =", targetUrl
        return targetUrl
    else:
        #print "not correct."
        return False

def correctUrl(url):
    for c in url:
        if not c in "&./0123456789=?ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnopqrstuvwxyz":
            return False
    return True

def bruteforce(min, max, exceptions):
    import itertools

    cand = []
    html = []
    
    for c in xrange(min, max+1):
        for p in itertools.permutations(indexbase, c):
            passwd = "".join(p)
            if not passwd in exceptions:
                targetUrl = ChkPwd(passwd)
                if targetUrl:
                    if targetUrl.endswith(".html"):
                        print "\a\aCracked!"
                        print "one of the hopeful answer is '%s'" % passwd
                        html.append((passwd, targetUrl))
                    if correctUrl(targetUrl):
                        print "One of the answer is '%s'" % passwd
                        cand.append((passwd, targetUrl))
                        #if raw_input("continue?(y/n)>") == "n": return
                else:
                    print

    else:
        if len(html) <= 0:
            if len(cand) <= 0:
                print "\a\aCouldn't find the answer."
                print "Prease set MAX to larger value."
            else:
                print "\a\a%d answers are found." % len(cand)
                print
                for p,url in cand:
                    print "Password:", p
                    print "URL:", url
                    print "--------"
        else:
            print "\a\a\a%d answers are found!" % len(html)
            print "which ends with '.html'!!"
            for p, url in html:
                print "Password:", p
                print "URL:", url
                print "========"
        return

class PWD(object):
    def __init__(self, p):
        # p is str
        self.pwd = p
        
    def get(self):
        return self.pwd

    def __repr__(self):
        return "PWD(%d)" % self.pwd

class PWDSET(object):
    def __init__(self, p1, p2):
        # p1 and p2 are instance of PWD
        if not ((type(p1) == PWD) or (type(p2) == PWD)):
            raise TypeErorr
        self.pwdset = [p1, p2]
        self.pwdset.sort()
        
    def get_all(self):
        return self.pwdset

    def has_pwd(self, p): 
        # p is instance of PWD
        
        for pwd in self.pwdset:
            if (type(pwd) == type(p)) and (p.get() == pwd.get()):
                return pwd
            
        return False

    def get_the_other(self, p):
        # p is instance of PWD
        r = self.has_pwd(p)
        if r:
            return self.pwdset[self.pwdset.index(r)-1]
        else:
            return None

    def is_same(self, pwdset):
        # pwdset is instance of pwdset
        p1, p2 = pwdset.get_all() # p1, p2 are PWD
        if self.has_pwd(p1) and self.has_pwd(p2):
            return True
        else:
            return False
        
    def __repr__(self):
        return "%s + %s" % (str(self.pwdset[0]), str(self.pwdset[1]))

class DATA(object):
    def __init__(self):
        self.pwdsets_values = []

    def has_key(self, pwdset):
        for ps,v in self.pwdsets_values:
            if ps.is_same(pwdset):
                return ps, v
        return None
    
    def has_pwd(self, pwd):
        for ps,v in self.pwdsets_values:
            if ps.has_pwd(pwd):
                yield ps, v
    
    def set(self, pwdset, value):
        av = self.has_key(pwdset)
        print "@DATA.set(%s, %d), " % (str(pwdset), value) + "av =", av
        if av:
            if value == av[1]:
                return True
            else:
                return False
        self.pwdsets_values.append((pwdset, value))
        return True
    
    def get(self, pwdset):
        for ps,v in self.pwdsets_values:
            if ps.is_same(pwdset):
                return v
            else:
                continue
        return False
    
    def get_both_pwd(self):
        for ps,v in self.pwdsets_values:
            if not False in [(type(p) == PWD) for p in ps.get_all()]:
                yield ps,v
                
    def print_all(self):
        for ps,v in self.pwdsets_values:
            print "%s = %d" % (str(ps), v)
        return

    def remove(self, pwdset, value):
        self.pwdsets_values.pop(self.pwdsets_values.index((pwdset,value)))
        return

class FPATH(object):
    def __init__(self, f):
        # f is str
        self.fpath = f

    def get(self):
        return self.fpath

    def __repr__(self):
        return "FPATH(%d)" % self.fpath

class KEY(object):
    def __init__(self):
        self.pwds_values = []
        
    def set(self, pwd, value):
        r = self.get(pwd)
        print "@KEY.set(%s, %d), " % (str(pwd), value) + "r =", r
        if r:
            if value == r:
                return True
            else:
                return False
        self.pwds_values.append((pwd, value))
        return True
    
    def get(self, pwd):
        for p,v in self.pwds_values:
            if (type(p) == type(pwd)) and (p.get() == pwd.get()):
                return v
        return False
    
    def get_all(self):
        return self.pwds_values
    
    def print_all(self):
        for p,v in self.pwds_values:
            print "%s = %d (%s)" % (str(p), v, indexbase[v])
        return

class PwdlenisNotN(Exception):
    def __init__(self, n):
        self.n = n

    def __str__(self):
        return "[*] Password length is not %d" % self.n

def hack(n=1):
    while n < len(keyString)-5: # 5 is for ".html"
        # パスワード長がnのとき
        j = [i for i in range(n)[::-1] * (len(keyString) / n) + range(n)[:len(keyString)%n-1:-1]]
        key = [PWD(i) for i in j]
        decrypted = [FPATH(i) for i in range(len(keyString)-5-n)] + [".", "h", "t", "m", "l"] + [PWD(i) for i in range(n)]
        unknown_data = DATA()
        encrypted = KEY()
        print "key:", key #
        print "j:", j #
        print "decrypted:", decrypted #
        try:
            for i,c in enumerate(keyString):
                print "-" * 10
                print "[*] i =", i
                print "[*] encrypted:"
                encrypted.print_all()
                print "[*] unknown_data:"
                unknown_data.print_all()

                if type(decrypted[i]) == str:
                    print "[*] %s = (%d - %d - %d) %% %d" % (str(key[i]), indexbase.index(c), j[i], indexbase.index(decrypted[i]), len(indexbase))
                    
                    if not encrypted.set(key[i], (indexbase.index(c) - j[i] - indexbase.index(decrypted[i])) % len(indexbase)):
                        #raise PwdlenisNotN(n)
                        pass
                    continue
                print c
                if not unknown_data.set(PWDSET(decrypted[i], key[i]), (indexbase.index(c)-j[i]) % len(indexbase)):
                    raise PwdlenisNotN(n)

        except PwdlenisNotN, e:
            print "[*] Password length is not %d" % e.n
            raw_input("<Password length = %d> is finished! continue?>" % n)
            n += 1
            continue
        print "[*] recheck"
        while c != 0:
            c = 0
            for p,v in encrypted.get_all():
                for ps,vs in unknown_data.has_pwd(p):
                    encrypted.set(ps.get_the_other(p), (vs - v) % len(indexbase))
                    c += 1
                    unknown_data.remove(ps, vs)
                
        print "=== Final result ==="
        encrypted.print_all()
        unknown_data.print_all()
        # show all patterns 
        # but now only for 2 char blanks
        passwd = ""
        brute = []
        for i in xrange(p):
            n = encrypted.get(PWD(i))
            if not p:
                passwd += "%c"##
                brute.append(i)
            else:
                passwd += indexbase[p]
        if len(brute) == 0:
            print "==== Password detected!! ===="
            print "PASSWORD =", passwd
        else:
            for ps,v in unknown_data.get_both_pwd()
            for i in brute:
                pwd = PWD(i)
                for ps,v in unknown_data.has_pwd(pwd):
                    o = ps.get_the_other(pwd).get()
                    if o < i:
                        print "==== Password candidates: ===="
                        for v_ in (v, v+len(indexbase)):
                            print passwd, o, i, v_
                            for c in range(len(indexbase)):
                                if len(indexbase) > v_-c:
                                    #password = passwd[:o] + indexbase[c] + passwd[o+1:i] + indexbase[v_-c] + passwd[i+1:]
                                    password  = passwd % (indexbase[c], indexbase[v_-c])
                                    url = ChkPwd(password)
                                    #if url:
                                    print "%s  (%s)" % (password, url)
                                
                        try:
                            brute.remove(o)
                        except ValueError:
                            pass
        
        raw_input("<Password length = %d> is finished! continue?>" % n)
        n += 1

def get_encrypted(url):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; ja; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3 ( .NET CLR 3.5.30729)')]
    source = opener.open(url).read()
    soup = BS(source)
    link = soup.find("a", {"onclick":re.compile(r"return _HpbPwdWnd.+")})
    if not link:
        return None
    m = re.match("return _HpbPwdWnd\(this,'(?P<code>.+)'\);$", link.get("onclick"))
    if not m:
        return None
    code = m.group("code")
    code = code.replace("\\'", "'") #
    return code

def print_usage(msg=None):
    if msg:
        print "Error!"
        print msg
        print
    print "Usage:"
    print "%s <URL or Encrypted Code> [<MIN_PASSWORD_LEN>]" % sys.argv[0]
    print "  URL = URL of the page which contains the link with password"
    print "  (Encrypted Code = 'return _HpbPwdWnd(this,<Encrypted Code>);')"
    print "  MIN_PASSWORD_LEN = minimum password length (optional/default is 1)"
    print

def main():
    global keyString
    if len(sys.argv[1:]) >= 1:
        if sys.argv[1].startswith("http"):
            p = get_encrypted(sys.argv[1])
            if not p:
                print_usage("Specific page does not contain the link with password!")
                return
        else:
            p = sys.argv[1]
        keyString = p
        print "Encrypted Code =", keyString
        if len(sys.argv[1:]) >= 2:
            hack(int(sys.argv[2]))
        else:
            hack()
    else:
        print_usage()

if __name__ == "__main__": main()
