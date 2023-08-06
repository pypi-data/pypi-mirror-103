import numpy as np #line:2
from copy import deepcopy #line:3
import matplotlib .pyplot as plt #line:4
import cv2 #line:5
def show (O00OO000O0000OOO0 ):#line:7
    plt .figure (figsize =(8 ,8 ))#line:8
    if np .max (O00OO000O0000OOO0 )==1 :#line:10
        plt .imshow (O00OO000O0000OOO0 ,vmin =0 ,vmax =1 )#line:11
    else :#line:12
        plt .imshow (O00OO000O0000OOO0 ,vmin =0 ,vmax =255 )#line:13
    plt .gray ()#line:14
    plt .show ()#line:15
    plt .close ()#line:16
    print ()#line:17
def resize (OOOO00OO0OO00OOO0 ,O0000000O00000OOO ):#line:19
    OO00O00O0O0O0OO00 ,OOOOOOO0OO0OO0O00 =OOOO00OO0OO00OOO0 .shape [:2 ]#line:21
    if OO00O00O0O0O0OO00 <OOOOOOO0OO0OO0O00 :#line:23
        OO00O00OO0O0OO00O =O0000000O00000OOO #line:24
        O0O0O0O0OOOO00O0O =int (OO00O00O0O0O0OO00 *O0000000O00000OOO /OOOOOOO0OO0OO0O00 )#line:25
        OO00OO00000OOOOOO =OOOOOOO0OO0OO0O00 /O0000000O00000OOO #line:26
    else :#line:27
        O0O0O0O0OOOO00O0O =O0000000O00000OOO #line:28
        OO00O00OO0O0OO00O =int (OOOOOOO0OO0OO0O00 *O0000000O00000OOO /OO00O00O0O0O0OO00 )#line:29
        OO00OO00000OOOOOO =OO00O00O0O0O0OO00 /O0000000O00000OOO #line:30
    OOOO00OO0OO00OOO0 =cv2 .resize (OOOO00OO0OO00OOO0 ,(OO00O00OO0O0OO00O ,O0O0O0O0OOOO00O0O ),interpolation =cv2 .INTER_CUBIC )#line:31
    print ('------------------------------------')#line:33
    print ('resizing in window size ({}, {})'.format (OO00O00OO0O0OO00O ,O0O0O0O0OOOO00O0O ))#line:34
    print ('(w, h) = ({}, {})'.format (OOOOOOO0OO0OO0O00 ,OO00O00O0O0O0OO00 ))#line:35
    print ('(w, h) = ({}, {})'.format (OO00O00OO0O0OO00O ,O0O0O0O0OOOO00O0O ))#line:36
    return OOOO00OO0OO00OOO0 ,OO00OO00000OOOOOO #line:37
class pointlist ():#line:39
    def __init__ (OOOO0OO0O00OO00O0 ):#line:40
        OOOO0OO0O00OO00O0 .points =[]#line:41
        OOOO0OO0O00OO00O0 .L =[]#line:42
        OOOO0OO0O00OO00O0 .R =[]#line:43
        OOOO0OO0O00OO00O0 .state =None #line:44
    def add (O0000000OO0OO00OO ,O0O00O000O0OOO00O ,OO00OO000OO0OO0O0 ,O0O0O0OO00O0O0O00 ):#line:46
        O0000000OO0OO00OO .points .append ([O0O00O000O0OOO00O ,OO00OO000OO0OO0O0 ])#line:47
        if O0O0O0OO00O0O0O00 =='L':#line:48
            O0000000OO0OO00OO .L .append ([O0O00O000O0OOO00O ,OO00OO000OO0OO0O0 ])#line:49
            O0000000OO0OO00OO .state ='L'#line:50
        if O0O0O0OO00O0O0O00 =='R':#line:51
            O0000000OO0OO00OO .R .append ([O0O00O000O0OOO00O ,OO00OO000OO0OO0O0 ])#line:52
            O0000000OO0OO00OO .state ='R'#line:53
        print ('points[{}] = ({}, {})'.format (len (O0000000OO0OO00OO .points )-1 ,O0O00O000O0OOO00O ,OO00OO000OO0OO0O0 ))#line:54
class vcclick :#line:56
    def __init__ (O0O00OO00O000O000 ):#line:57
        pass #line:58
    def __del__ (OO0O000O000OO0O0O ):#line:59
        pass #line:60
    def get_draw (O0000O000OOO00O0O ,return_size ='original'):#line:62
        if return_size =='original':#line:63
            O0000O000OOO00O0O .img_draw_original =cv2 .resize (O0000O000OOO00O0O .img_draw ,O0000O000OOO00O0O .img_original .shape [:2 ][::-1 ],interpolation =cv2 .INTER_CUBIC )#line:64
            return O0000O000OOO00O0O .img_draw_original #line:65
        else :#line:66
            return O0000O000OOO00O0O .img_draw #line:67
    def get_mask (O0OO00OO0OO00OO0O ,return_size ='original'):#line:69
        if O0OO00OO0OO00OO0O .mode =='single':#line:70
            if return_size =='original':#line:71
                OOO00O00O000O0OO0 =np .zeros (O0OO00OO0OO00OO0O .img_original .shape ,int )#line:72
                OO0OO000O00OOOO0O =np .array (O0OO00OO0OO00OO0O .points .points )*O0OO00OO0OO00OO0O .rate #line:73
                OO0OO000O00OOOO0O =OO0OO000O00OOOO0O .astype (int )#line:74
                cv2 .fillConvexPoly (OOO00O00O000O0OO0 ,points =OO0OO000O00OOOO0O ,color =(1 ,1 ,1 ))#line:75
            else :#line:76
                OOO00O00O000O0OO0 =np .zeros (O0OO00OO0OO00OO0O .img .shape ,int )#line:77
                OO0OO000O00OOOO0O =np .array (O0OO00OO0OO00OO0O .points .points )#line:78
                cv2 .fillConvexPoly (OOO00O00O000O0OO0 ,points =OO0OO000O00OOOO0O ,color =(1 ,1 ,1 ))#line:79
        if O0OO00OO0OO00OO0O .mode =='multi':#line:80
            if return_size =='original':#line:81
                OOO00O00O000O0OO0 =np .zeros (O0OO00OO0OO00OO0O .img_original .shape ,int )#line:82
                for O0OO00O0O0OO0OO00 in O0OO00OO0OO00OO0O .points_set :#line:84
                    OO0OO000O00OOOO0O =np .array (O0OO00O0O0OO0OO00 )*O0OO00OO0OO00OO0O .rate #line:85
                    OO0OO000O00OOOO0O =OO0OO000O00OOOO0O .astype (int )#line:86
                    cv2 .fillConvexPoly (OOO00O00O000O0OO0 ,points =OO0OO000O00OOOO0O ,color =(1 ,1 ,1 ))#line:87
            else :#line:88
                OOO00O00O000O0OO0 =np .zeros (O0OO00OO0OO00OO0O .img .shape ,int )#line:89
                for O0OO00O0O0OO0OO00 in O0OO00OO0OO00OO0O .points_set :#line:91
                    OO0OO000O00OOOO0O =np .array (O0OO00O0O0OO0OO00 )#line:92
                    cv2 .fillConvexPoly (OOO00O00O000O0OO0 ,points =OO0OO000O00OOOO0O ,color =(1 ,1 ,1 ))#line:93
        OOO00O00O000O0OO0 =np .sum (OOO00O00O000O0OO0 ,axis =2 )==3 #line:94
        return OOO00O00O000O0OO0 #line:95
    def single (O0000OO00O0OO0O00 ,O00OO0OOOOOOOO000 ,window_size =1000 ,guide =(0 ,255 ,0 ),marker =(255 ,0 ,0 ),line =(0 ,255 ,0 ),return_size ='original'):#line:101
        O0000OO00O0OO0O00 .img_original =np .array (O00OO0OOOOOOOO000 )#line:103
        O0000OO00O0OO0O00 .window_size =window_size #line:104
        assert guide ==None or len (guide )==3 #line:105
        assert marker ==None or len (marker )==3 #line:106
        assert line ==None or len (line )==3 #line:107
        O0000OO00O0OO0O00 .guide =guide [::-1 ]if guide !=None else None #line:108
        O0000OO00O0OO0O00 .marker =marker [::-1 ]if marker !=None else None #line:109
        O0000OO00O0OO0O00 .line =line [::-1 ]if line !=None else None #line:110
        O0000OO00O0OO0O00 .points =pointlist ()#line:111
        O0000OO00O0OO0O00 .points_set =[]#line:112
        O0000OO00O0OO0O00 .wname ='aaa'#line:113
        O0000OO00O0OO0O00 .img ,O0000OO00O0OO0O00 .rate =resize (O0000OO00O0OO0O00 .img_original ,O0000OO00O0OO0O00 .window_size )#line:116
        O0000OO00O0OO0O00 .h ,O0000OO00O0OO0O00 .w =O0000OO00O0OO0O00 .img .shape [:2 ]#line:118
        O0000OO00O0OO0O00 .img_draw =deepcopy (O0000OO00O0OO0O00 .img )#line:119
        O0000OO00O0OO0O00 .mode ='single'#line:122
        cv2 .namedWindow (O0000OO00O0OO0O00 .wname )#line:123
        cv2 .setMouseCallback (O0000OO00O0OO0O00 .wname ,O0000OO00O0OO0O00 .start )#line:124
        cv2 .imshow (O0000OO00O0OO0O00 .wname ,O0000OO00O0OO0O00 .img )#line:126
        cv2 .waitKey ()#line:127
        if return_size =='original':#line:130
            print ('return in original size {}'.format (O0000OO00O0OO0O00 .img_original .shape [:2 ][::-1 ]))#line:131
            print ('------------------------------------')#line:132
            return np .array (O0000OO00O0OO0O00 .points .points )*O0000OO00O0OO0O00 .rate #line:133
        else :#line:134
            print ('return in window size {}'.format (O0000OO00O0OO0O00 .img .shape [:2 ][::-1 ]))#line:135
            return np .array (O0000OO00O0OO0O00 .points .points )#line:136
    def multi (O000O0O00O00000OO ,O000O0OO00OO0O0O0 ,window_size =1000 ,guide =(0 ,255 ,0 ),marker =(255 ,0 ,0 ),line =(0 ,255 ,0 ),return_size ='original'):#line:142
        O000O0O00O00000OO .img_original =np .array (O000O0OO00OO0O0O0 )#line:144
        O000O0O00O00000OO .window_size =window_size #line:145
        assert guide ==None or len (guide )==3 #line:146
        assert marker ==None or len (marker )==3 #line:147
        assert line ==None or len (line )==3 #line:148
        O000O0O00O00000OO .guide =guide [::-1 ]if guide !=None else None #line:149
        O000O0O00O00000OO .marker =marker [::-1 ]if marker !=None else None #line:150
        O000O0O00O00000OO .line =line [::-1 ]if line !=None else None #line:151
        O000O0O00O00000OO .points =pointlist ()#line:152
        O000O0O00O00000OO .points_set =[]#line:153
        O000O0O00O00000OO .wname ='aaa'#line:154
        O000O0O00O00000OO .img ,O000O0O00O00000OO .rate =resize (O000O0O00O00000OO .img_original ,O000O0O00O00000OO .window_size )#line:157
        O000O0O00O00000OO .h ,O000O0O00O00000OO .w =O000O0O00O00000OO .img .shape [:2 ]#line:159
        O000O0O00O00000OO .img_draw =deepcopy (O000O0O00O00000OO .img )#line:160
        O000O0O00O00000OO .mode ='multi'#line:163
        cv2 .namedWindow (O000O0O00O00000OO .wname )#line:164
        cv2 .setMouseCallback (O000O0O00O00000OO .wname ,O000O0O00O00000OO .start )#line:165
        cv2 .imshow (O000O0O00O00000OO .wname ,O000O0O00O00000OO .img )#line:167
        cv2 .waitKey ()#line:168
        if return_size =='original':#line:171
            print ('return in original size {}'.format (O000O0O00O00000OO .img_original .shape [:2 ][::-1 ]))#line:172
            print ('------------------------------------')#line:173
            O000O0O0OO0OO0OOO =deepcopy (O000O0O00O00000OO .points_set )#line:174
            for OO0O0O00OOO0OOOOO in range (len (O000O0O0OO0OO0OOO )):#line:175
                O000O0O0OO0OO0OOO [OO0O0O00OOO0OOOOO ]=np .array (O000O0O0OO0OO0OOO [OO0O0O00OOO0OOOOO ])*O000O0O00O00000OO .rate #line:176
            return O000O0O0OO0OO0OOO #line:177
        else :#line:178
            print ('return in window size {}'.format (O000O0O00O00000OO .img .shape [:2 ][::-1 ]))#line:179
            O000O0O0OO0OO0OOO =deepcopy (O000O0O00O00000OO .points_set )#line:180
            for OO0O0O00OOO0OOOOO in range (len (O000O0O0OO0OO0OOO )):#line:181
                O000O0O0OO0OO0OOO [OO0O0O00OOO0OOOOO ]=np .array (O000O0O0OO0OO0OOO [OO0O0O00OOO0OOOOO ])#line:182
            return O000O0O00O00000OO .points_set #line:183
    def start (O0000OOO00OOOOOO0 ,OOO0O0O0O0O0OOO0O ,O00OOOOOOO0OO00O0 ,O0O00O0OO00O0O0O0 ,OO0OO000O0O0OOO00 ,OOO0OOOO0O000O00O ):#line:186
        if OOO0O0O0O0O0OOO0O ==cv2 .EVENT_MBUTTONDOWN :#line:188
            cv2 .destroyAllWindows ()#line:189
        if OOO0O0O0O0O0OOO0O ==cv2 .EVENT_MOUSEMOVE :#line:192
            OOOO0O0OO00O00OOO =deepcopy (O0000OOO00OOOOOO0 .img_draw )#line:194
            if O0000OOO00OOOOOO0 .guide !=None :#line:196
                cv2 .line (OOOO0O0OO00O00OOO ,(O00OOOOOOO0OO00O0 ,0 ),(O00OOOOOOO0OO00O0 ,O0000OOO00OOOOOO0 .h -1 ),O0000OOO00OOOOOO0 .guide )#line:197
                cv2 .line (OOOO0O0OO00O00OOO ,(0 ,O0O00O0OO00O0O0O0 ),(O0000OOO00OOOOOO0 .w -1 ,O0O00O0OO00O0O0O0 ),O0000OOO00OOOOOO0 .guide )#line:198
            if O0000OOO00OOOOOO0 .points .state =='L':#line:200
                if O0000OOO00OOOOOO0 .line !=None :#line:201
                    OO000OOO0000OO0OO ,OOO0O000O00O0OO0O =O0000OOO00OOOOOO0 .points .L [-1 ]#line:202
                    cv2 .line (OOOO0O0OO00O00OOO ,(OO000OOO0000OO0OO ,OOO0O000O00O0OO0O ),(O00OOOOOOO0OO00O0 ,O0O00O0OO00O0O0O0 ),O0000OOO00OOOOOO0 .guide )#line:203
            cv2 .imshow (O0000OOO00OOOOOO0 .wname ,OOOO0O0OO00O00OOO )#line:205
        if OOO0O0O0O0O0OOO0O ==cv2 .EVENT_LBUTTONDOWN :#line:208
            if O0000OOO00OOOOOO0 .points .state =='L':#line:210
                cv2 .circle (O0000OOO00OOOOOO0 .img_draw ,(O00OOOOOOO0OO00O0 ,O0O00O0OO00O0O0O0 ),4 ,O0000OOO00OOOOOO0 .marker ,1 )#line:212
                if O0000OOO00OOOOOO0 .line !=None :#line:214
                    OO000OOO0000OO0OO ,OOO0O000O00O0OO0O =O0000OOO00OOOOOO0 .points .L [-1 ]#line:215
                    cv2 .line (O0000OOO00OOOOOO0 .img_draw ,(OO000OOO0000OO0OO ,OOO0O000O00O0OO0O ),(O00OOOOOOO0OO00O0 ,O0O00O0OO00O0O0O0 ),O0000OOO00OOOOOO0 .line )#line:216
                O0000OOO00OOOOOO0 .points .add (O00OOOOOOO0OO00O0 ,O0O00O0OO00O0O0O0 ,'L')#line:218
                cv2 .imshow (O0000OOO00OOOOOO0 .wname ,O0000OOO00OOOOOO0 .img_draw )#line:220
            else :#line:222
                O0000OOO00OOOOOO0 .points .add (O00OOOOOOO0OO00O0 ,O0O00O0OO00O0O0O0 ,'L')#line:224
                cv2 .circle (O0000OOO00OOOOOO0 .img_draw ,(O00OOOOOOO0OO00O0 ,O0O00O0OO00O0O0O0 ),4 ,O0000OOO00OOOOOO0 .marker ,1 )#line:226
                cv2 .imshow (O0000OOO00OOOOOO0 .wname ,O0000OOO00OOOOOO0 .img_draw )#line:228
        if OOO0O0O0O0O0OOO0O ==cv2 .EVENT_RBUTTONDOWN :#line:231
            if O0000OOO00OOOOOO0 .points .state =='L':#line:233
                cv2 .circle (O0000OOO00OOOOOO0 .img_draw ,(O00OOOOOOO0OO00O0 ,O0O00O0OO00O0O0O0 ),4 ,O0000OOO00OOOOOO0 .marker ,1 )#line:235
                if O0000OOO00OOOOOO0 .line !=None :#line:237
                    OO000OOO0000OO0OO ,OOO0O000O00O0OO0O =O0000OOO00OOOOOO0 .points .L [-1 ]#line:238
                    cv2 .line (O0000OOO00OOOOOO0 .img_draw ,(OO000OOO0000OO0OO ,OOO0O000O00O0OO0O ),(O00OOOOOOO0OO00O0 ,O0O00O0OO00O0O0O0 ),O0000OOO00OOOOOO0 .line )#line:239
                O0000OOO00OOOOOO0 .points .add (O00OOOOOOO0OO00O0 ,O0O00O0OO00O0O0O0 ,'R')#line:241
                cv2 .imshow (O0000OOO00OOOOOO0 .wname ,O0000OOO00OOOOOO0 .img_draw )#line:243
                if O0000OOO00OOOOOO0 .mode =='multi':#line:246
                    O0000OOO00OOOOOO0 .points_set .append (O0000OOO00OOOOOO0 .points .points )#line:247
                    O0000OOO00OOOOOO0 .points =pointlist ()#line:248
            else :#line:251
                pass #line:252
            if O0000OOO00OOOOOO0 .mode =='single':#line:255
                cv2 .destroyAllWindows ()#line:256
if __name__ =='__main__':#line:259
    file_name ='yoko.JPG'#line:261
    img =cv2 .imread (file_name )#line:266
    show (img )#line:267
    myclick =vcclick ()#line:270
    points =myclick .multi (img )#line:271
    print (points )#line:272
    img_mark =myclick .get_draw ()#line:274
    show (img_mark )#line:275
    mask =myclick .get_mask ()#line:277
    show (mask )#line:278
