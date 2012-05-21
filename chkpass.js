function _HpbChkPwd(keyin,escEncrypted,defaultUrl,target)
{
    var	encrypted = unescape(escEncrypted);
    var indexbase = " !\"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~";
    var passlen = keyin.length;
    var enqlen  = encrypted.length;
    var decrypted = "";
    var decryptedPassword = "";
    var decryptedPath     = "";
    var targetUrl         = "";
    var i, j, k, chr1, chr2, nbase;
    var needPassword = "%u30D1%u30B9%u30EF%u30FC%u30C9%u3092%u5165%u529B%u3057%u3066%u304F%u3060%u3055%u3044%u3002";
    var badPassword  = "%u30D1%u30B9%u30EF%u30FC%u30C9%u304C%u6B63%u3057%u304F%u3042%u308A%u307E%u305B%u3093%u3002";
    if (passlen <= 0)
    {
	alert(unescape(needPassword));
	//return ;
    }
    console.log("encrypted:", encrypted);
    console.log("keyin:", keyin);
    console.log("indexbase:", indexbase);
    for (i = 0, j = passlen - 1, k = 0 ; i < enqlen ; i++, j--, k=0)
    {
	if (j < 0)
	{
	    j = passlen - 1;
	}
	chr1 = indexbase.indexOf(keyin.charAt(j));
	chr2 = indexbase.indexOf(encrypted.charAt(i));
	console.log("j:", j, "keyin.charAt(j):", keyin.charAt(j));
	console.log("chr1:", chr1);
	console.log("i:", i, "encrypted.charAt(i):", encrypted.charAt(i));
	console.log("chr2:", chr2);
	console.log("----------");
	if (chr2 < (chr1 + j))
	{
	    nbase = (chr1 + j - chr2) / 0x5f;
	    k += (0x5f * Math.ceil(nbase));
	}
	k += (chr2 - chr1 - j);
	decrypted += indexbase.charAt(k);
    }
    decryptedPassword = decrypted.substring(decrypted.length - passlen, decrypted.length);
    console.log("decrypted:", decrypted);
    console.log("decryptedPassword:", decryptedPassword);
    if (keyin == decryptedPassword)
    {
	decryptedPath = decrypted.substring(0, decrypted.length - passlen);
	console.log("decryptedPath:", decryptedPath);
	passlen       = decryptedPath.length;
	for (i = 0 ; i < passlen ; i++)
	{
	    chr1 = decryptedPath.charAt(i);
	    if (chr1 == "%")
	    {
		chr2 = decryptedPath.substring(i, i+6);
		targetUrl += chr2;
		i += 11;
	    }
	    else
		targetUrl += chr1;
	}
	//location.href = targetUrl;
	//window.close();
	console.log("location.href=[targetUrl=" + targetUrl + "]");
    }
    else
    {
	if (defaultUrl.length)
	{
	    //location.href = defaultUrl;
	    console.log("location.href=[defaultUrl=" + defaultUrl+"]");
	}
	else
	{
	    alert(unescape(badPassword));
	}
	//window.close();
    }
}
