from hmac import new as hmac
from hashlib import sha256

#Please insert your own secret key here
secret = '909586a7e5594e00a58e2a26c107f9cb'

class Checksum:

    def __init__(self,postdata):
        self.post_data = postdata

    def calculateChecksum(self, secret_key, all):
        """Uses an HMAC SHA-256 algorithm to calculate the checksum
         of the data passed."""
        
        checksum = hmac(secret_key, all, sha256).hexdigest()
        return str(checksum)

    def getAllParams(self):
        """Concatenates and returns the NVP((Name-Value Pairs) in the POST data as a single string."""
        
        all = ''
        for key in sorted(self.post_data.iterkeys()):
            if(key != 'checksum'):
                all += "'" + self.post_data[key] + "'"
        return all

    def outputForm(self, checksum):
        """Outputs the hidden form for POSTing the data to the Zaakpay API."""
        
        a = ''
        for key in sorted(self.post_data.iterkeys()):
            a += '<input type="hidden" name="' + key + '"value="' + self.post_data[key] + '"/>' + "\n"

        a += '<input type="hidden" name = "checksum" value="' + checksum + '" />' + "\n"
        return a

    def verifyChecksum(self, checksum, all, secret):
        """Verifies if the checksum provided and the actual one match."""

        cal_checksum = self.calculateChecksum(secret, all)
        if(checksum == cal_checksum):
            return 1
        return 0
    
    def outputResponse(self, bool):

        a = ''
        for key in self.post_data.iterkeys():
            a += '<tr><td width="50%" align="center" valign="middle">' + key + '</td>\
                    <td width="50%" align="center" valign="middle">' + self.post_data[key] + '</td>\
                    </tr>'
        
        a += '<tr><td width="50%" align="center" valign="middle">Checksum Verified?</td>'
        
        if(bool == 1):
                a += '<td width="50%" align="center" valign="middle">Yes</td></tr>'
        else: 
            a += '<td width="50%" align="center" valign="middle">No</td></tr>'
        return a