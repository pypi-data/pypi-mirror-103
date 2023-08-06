import numpy as np #line:2
from copy import deepcopy #line:3
import matplotlib .pyplot as plt #line:4
import cv2 #line:5
def show (O000OOOOOO0O00OOO ):#line:7
    plt .figure (figsize =(8 ,8 ))#line:8
    if np .max (O000OOOOOO0O00OOO )==1 :#line:10
        plt .imshow (O000OOOOOO0O00OOO ,vmin =0 ,vmax =1 )#line:11
    else :#line:12
        plt .imshow (O000OOOOOO0O00OOO ,vmin =0 ,vmax =255 )#line:13
    plt .gray ()#line:14
    plt .show ()#line:15
    plt .close ()#line:16
    print ()#line:17
def resize (OO0O00O0000O00OOO ,O0000OOO0O0OOO0O0 ):#line:19
    OOOO0OO0OOOOO0O00 ,O0000O0O0OO00O0O0 =OO0O00O0000O00OOO .shape [:2 ]#line:21
    if OOOO0OO0OOOOO0O00 <O0000O0O0OO00O0O0 :#line:23
        O0O0O00O0000OOOO0 =O0000OOO0O0OOO0O0 #line:24
        OO00O0OO0OOOO0O0O =int (OOOO0OO0OOOOO0O00 *O0000OOO0O0OOO0O0 /O0000O0O0OO00O0O0 )#line:25
        OOO0O0OO0OOO0O0OO =O0000O0O0OO00O0O0 /O0000OOO0O0OOO0O0 #line:26
    else :#line:27
        OO00O0OO0OOOO0O0O =O0000OOO0O0OOO0O0 #line:28
        O0O0O00O0000OOOO0 =int (O0000O0O0OO00O0O0 *O0000OOO0O0OOO0O0 /OOOO0OO0OOOOO0O00 )#line:29
        OOO0O0OO0OOO0O0OO =OOOO0OO0OOOOO0O00 /O0000OOO0O0OOO0O0 #line:30
    OO0O00O0000O00OOO =cv2 .resize (OO0O00O0000O00OOO ,(O0O0O00O0000OOOO0 ,OO00O0OO0OOOO0O0O ),interpolation =cv2 .INTER_CUBIC )#line:31
    print ('------------------------------------')#line:33
    print ('resizing in window size ({}, {})'.format (O0O0O00O0000OOOO0 ,OO00O0OO0OOOO0O0O ))#line:34
    print ('(w, h) = ({}, {})'.format (O0000O0O0OO00O0O0 ,OOOO0OO0OOOOO0O00 ))#line:35
    print ('(w, h) = ({}, {})'.format (O0O0O00O0000OOOO0 ,OO00O0OO0OOOO0O0O ))#line:36
    return OO0O00O0000O00OOO ,OOO0O0OO0OOO0O0OO #line:37
class pointlist ():#line:39
    def __init__ (OOOO0O0000000OOOO ):#line:40
        OOOO0O0000000OOOO .points =[]#line:41
        OOOO0O0000000OOOO .L =[]#line:42
        OOOO0O0000000OOOO .R =[]#line:43
        OOOO0O0000000OOOO .state =None #line:44
    def add (OO0OOO000OOOO00OO ,O00OOO0OO00OO00O0 ,O00O00O00O00O00O0 ,OO000OO0OO0O00OOO ):#line:46
        OO0OOO000OOOO00OO .points .append ([O00OOO0OO00OO00O0 ,O00O00O00O00O00O0 ])#line:47
        if OO000OO0OO0O00OOO =='L':#line:48
            OO0OOO000OOOO00OO .L .append ([O00OOO0OO00OO00O0 ,O00O00O00O00O00O0 ])#line:49
            OO0OOO000OOOO00OO .state ='L'#line:50
        if OO000OO0OO0O00OOO =='R':#line:51
            OO0OOO000OOOO00OO .R .append ([O00OOO0OO00OO00O0 ,O00O00O00O00O00O0 ])#line:52
            OO0OOO000OOOO00OO .state ='R'#line:53
        print ('points[{}] = ({}, {})'.format (len (OO0OOO000OOOO00OO .points )-1 ,O00OOO0OO00OO00O0 ,O00O00O00O00O00O0 ))#line:54
class vcclick :#line:56
    def __init__ (O0O00000O0O0000OO ):#line:57
        pass #line:58
    def __del__ (O00OOO0OO0O0000O0 ):#line:59
        pass #line:60
    def get_draw (OOOO0OOOOO00OO000 ,return_size ='original'):#line:62
        if return_size =='original':#line:63
            OOOO0OOOOO00OO000 .img_draw_original =cv2 .resize (OOOO0OOOOO00OO000 .img_draw ,OOOO0OOOOO00OO000 .img_original .shape [:2 ][::-1 ],interpolation =cv2 .INTER_CUBIC )#line:64
            return OOOO0OOOOO00OO000 .img_draw_original #line:65
        else :#line:66
            return OOOO0OOOOO00OO000 .img_draw #line:67
    def get_mask (O0OOO00O0O00OO00O ,return_size ='original'):#line:69
        if O0OOO00O0O00OO00O .mode =='single':#line:70
            if return_size =='original':#line:71
                OOO00O0OO00OO0000 =np .zeros (O0OOO00O0O00OO00O .img_original .shape ,int )#line:72
                O0O00O00OOO000000 =np .array (O0OOO00O0O00OO00O .points .points )*O0OOO00O0O00OO00O .rate #line:73
                O0O00O00OOO000000 =O0O00O00OOO000000 .astype (int )#line:74
                cv2 .fillConvexPoly (OOO00O0OO00OO0000 ,points =O0O00O00OOO000000 ,color =(1 ,1 ,1 ))#line:75
            else :#line:76
                OOO00O0OO00OO0000 =np .zeros (O0OOO00O0O00OO00O .img .shape ,int )#line:77
                O0O00O00OOO000000 =np .array (O0OOO00O0O00OO00O .points .points )#line:78
                cv2 .fillConvexPoly (OOO00O0OO00OO0000 ,points =O0O00O00OOO000000 ,color =(1 ,1 ,1 ))#line:79
        if O0OOO00O0O00OO00O .mode =='multi':#line:80
            if return_size =='original':#line:81
                OOO00O0OO00OO0000 =np .zeros (O0OOO00O0O00OO00O .img_original .shape ,int )#line:82
                for OO0O00O00OO0OO0OO in O0OOO00O0O00OO00O .points_set :#line:84
                    O0O00O00OOO000000 =np .array (OO0O00O00OO0OO0OO )*O0OOO00O0O00OO00O .rate #line:85
                    O0O00O00OOO000000 =O0O00O00OOO000000 .astype (int )#line:86
                    cv2 .fillConvexPoly (OOO00O0OO00OO0000 ,points =O0O00O00OOO000000 ,color =(1 ,1 ,1 ))#line:87
            else :#line:88
                OOO00O0OO00OO0000 =np .zeros (O0OOO00O0O00OO00O .img .shape ,int )#line:89
                for OO0O00O00OO0OO0OO in O0OOO00O0O00OO00O .points_set :#line:91
                    O0O00O00OOO000000 =np .array (OO0O00O00OO0OO0OO )#line:92
                    cv2 .fillConvexPoly (OOO00O0OO00OO0000 ,points =O0O00O00OOO000000 ,color =(1 ,1 ,1 ))#line:93
        OOO00O0OO00OO0000 =np .sum (OOO00O0OO00OO0000 ,axis =2 )==3 #line:94
        return OOO00O0OO00OO0000 #line:95
    def single (O0OO00OOO0OO0O0O0 ,O0OO0O000O00O0OO0 ,window_size =1000 ,guide =(0 ,255 ,0 ),marker =(255 ,0 ,0 ),line =(0 ,255 ,0 ),return_size ='original'):#line:101
        O0OO00OOO0OO0O0O0 .img_original =np .array (O0OO0O000O00O0OO0 )#line:103
        O0OO00OOO0OO0O0O0 .window_size =window_size #line:104
        assert guide ==None or len (guide )==3 #line:105
        assert marker ==None or len (marker )==3 #line:106
        assert line ==None or len (line )==3 #line:107
        O0OO00OOO0OO0O0O0 .guide =guide [::-1 ]if guide !=None else None #line:108
        O0OO00OOO0OO0O0O0 .marker =marker [::-1 ]if marker !=None else None #line:109
        O0OO00OOO0OO0O0O0 .line =line [::-1 ]if line !=None else None #line:110
        O0OO00OOO0OO0O0O0 .points =pointlist ()#line:111
        O0OO00OOO0OO0O0O0 .points_set =[]#line:112
        O0OO00OOO0OO0O0O0 .wname ='aaa'#line:113
        O0OO00OOO0OO0O0O0 .img ,O0OO00OOO0OO0O0O0 .rate =resize (O0OO00OOO0OO0O0O0 .img_original ,O0OO00OOO0OO0O0O0 .window_size )#line:116
        O0OO00OOO0OO0O0O0 .h ,O0OO00OOO0OO0O0O0 .w =O0OO00OOO0OO0O0O0 .img .shape [:2 ]#line:118
        O0OO00OOO0OO0O0O0 .img_draw =deepcopy (O0OO00OOO0OO0O0O0 .img )#line:119
        O0OO00OOO0OO0O0O0 .mode ='single'#line:122
        cv2 .namedWindow (O0OO00OOO0OO0O0O0 .wname )#line:123
        cv2 .setMouseCallback (O0OO00OOO0OO0O0O0 .wname ,O0OO00OOO0OO0O0O0 .start )#line:124
        cv2 .imshow (O0OO00OOO0OO0O0O0 .wname ,O0OO00OOO0OO0O0O0 .img )#line:126
        cv2 .waitKey ()#line:127
        if return_size =='original':#line:130
            print ('return in original size {}'.format (O0OO00OOO0OO0O0O0 .img_original .shape [:2 ][::-1 ]))#line:131
            print ('------------------------------------')#line:132
            return np .array (O0OO00OOO0OO0O0O0 .points .points )*O0OO00OOO0OO0O0O0 .rate #line:133
        else :#line:134
            print ('return in window size {}'.format (O0OO00OOO0OO0O0O0 .img .shape [:2 ][::-1 ]))#line:135
            return np .array (O0OO00OOO0OO0O0O0 .points .points )#line:136
    def multi (OO0OO0000000O00OO ,O0OO000OO0O0O000O ,window_size =1000 ,guide =(0 ,255 ,0 ),marker =(255 ,0 ,0 ),line =(0 ,255 ,0 ),return_size ='original'):#line:142
        OO0OO0000000O00OO .img_original =np .array (O0OO000OO0O0O000O )#line:144
        OO0OO0000000O00OO .window_size =window_size #line:145
        assert guide ==None or len (guide )==3 #line:146
        assert marker ==None or len (marker )==3 #line:147
        assert line ==None or len (line )==3 #line:148
        OO0OO0000000O00OO .guide =guide [::-1 ]if guide !=None else None #line:149
        OO0OO0000000O00OO .marker =marker [::-1 ]if marker !=None else None #line:150
        OO0OO0000000O00OO .line =line [::-1 ]if line !=None else None #line:151
        OO0OO0000000O00OO .points =pointlist ()#line:152
        OO0OO0000000O00OO .points_set =[]#line:153
        OO0OO0000000O00OO .wname ='aaa'#line:154
        OO0OO0000000O00OO .img ,OO0OO0000000O00OO .rate =resize (OO0OO0000000O00OO .img_original ,OO0OO0000000O00OO .window_size )#line:157
        OO0OO0000000O00OO .h ,OO0OO0000000O00OO .w =OO0OO0000000O00OO .img .shape [:2 ]#line:159
        OO0OO0000000O00OO .img_draw =deepcopy (OO0OO0000000O00OO .img )#line:160
        OO0OO0000000O00OO .mode ='multi'#line:163
        cv2 .namedWindow (OO0OO0000000O00OO .wname )#line:164
        cv2 .setMouseCallback (OO0OO0000000O00OO .wname ,OO0OO0000000O00OO .start )#line:165
        cv2 .imshow (OO0OO0000000O00OO .wname ,OO0OO0000000O00OO .img )#line:167
        cv2 .waitKey ()#line:168
        if return_size =='original':#line:171
            print ('return in original size {}'.format (OO0OO0000000O00OO .img_original .shape [:2 ][::-1 ]))#line:172
            print ('------------------------------------')#line:173
            O0O0OOO00O000OO0O =deepcopy (OO0OO0000000O00OO .points_set )#line:174
            for OOO0O0O0O00O0O0OO in range (len (O0O0OOO00O000OO0O )):#line:175
                O0O0OOO00O000OO0O [OOO0O0O0O00O0O0OO ]=np .array (O0O0OOO00O000OO0O [OOO0O0O0O00O0O0OO ])*OO0OO0000000O00OO .rate #line:176
            return O0O0OOO00O000OO0O #line:177
        else :#line:178
            print ('return in window size {}'.format (OO0OO0000000O00OO .img .shape [:2 ][::-1 ]))#line:179
            O0O0OOO00O000OO0O =deepcopy (OO0OO0000000O00OO .points_set )#line:180
            for OOO0O0O0O00O0O0OO in range (len (O0O0OOO00O000OO0O )):#line:181
                O0O0OOO00O000OO0O [OOO0O0O0O00O0O0OO ]=np .array (O0O0OOO00O000OO0O [OOO0O0O0O00O0O0OO ])#line:182
            return OO0OO0000000O00OO .points_set #line:183
    def start (O000O000OOOOO00OO ,O0000000OO0OO00O0 ,O0O00O0OO000O0OO0 ,O00000O0OO0O0OO00 ,OO0O0O00OOOO0O00O ,O00OOOOOO0O000000 ):#line:186
        if O0000000OO0OO00O0 ==cv2 .EVENT_MBUTTONDOWN :#line:188
            cv2 .destroyWindow ('aaa')#line:189
        if O0000000OO0OO00O0 ==cv2 .EVENT_MOUSEMOVE :#line:192
            OOOOOO0O0O000O0O0 =deepcopy (O000O000OOOOO00OO .img_draw )#line:194
            if O000O000OOOOO00OO .guide !=None :#line:196
                cv2 .line (OOOOOO0O0O000O0O0 ,(O0O00O0OO000O0OO0 ,0 ),(O0O00O0OO000O0OO0 ,O000O000OOOOO00OO .h -1 ),O000O000OOOOO00OO .guide )#line:197
                cv2 .line (OOOOOO0O0O000O0O0 ,(0 ,O00000O0OO0O0OO00 ),(O000O000OOOOO00OO .w -1 ,O00000O0OO0O0OO00 ),O000O000OOOOO00OO .guide )#line:198
            if O000O000OOOOO00OO .points .state =='L':#line:200
                if O000O000OOOOO00OO .line !=None :#line:201
                    O0OO0O0000O00OO0O ,O0O0O0O0OOOO0OO0O =O000O000OOOOO00OO .points .L [-1 ]#line:202
                    cv2 .line (OOOOOO0O0O000O0O0 ,(O0OO0O0000O00OO0O ,O0O0O0O0OOOO0OO0O ),(O0O00O0OO000O0OO0 ,O00000O0OO0O0OO00 ),O000O000OOOOO00OO .guide )#line:203
            cv2 .imshow (O000O000OOOOO00OO .wname ,OOOOOO0O0O000O0O0 )#line:205
        if O0000000OO0OO00O0 ==cv2 .EVENT_LBUTTONDOWN :#line:208
            if O000O000OOOOO00OO .points .state =='L':#line:210
                cv2 .circle (O000O000OOOOO00OO .img_draw ,(O0O00O0OO000O0OO0 ,O00000O0OO0O0OO00 ),4 ,O000O000OOOOO00OO .marker ,1 )#line:212
                if O000O000OOOOO00OO .line !=None :#line:214
                    O0OO0O0000O00OO0O ,O0O0O0O0OOOO0OO0O =O000O000OOOOO00OO .points .L [-1 ]#line:215
                    cv2 .line (O000O000OOOOO00OO .img_draw ,(O0OO0O0000O00OO0O ,O0O0O0O0OOOO0OO0O ),(O0O00O0OO000O0OO0 ,O00000O0OO0O0OO00 ),O000O000OOOOO00OO .line )#line:216
                O000O000OOOOO00OO .points .add (O0O00O0OO000O0OO0 ,O00000O0OO0O0OO00 ,'L')#line:218
                cv2 .imshow (O000O000OOOOO00OO .wname ,O000O000OOOOO00OO .img_draw )#line:220
            else :#line:222
                O000O000OOOOO00OO .points .add (O0O00O0OO000O0OO0 ,O00000O0OO0O0OO00 ,'L')#line:224
                cv2 .circle (O000O000OOOOO00OO .img_draw ,(O0O00O0OO000O0OO0 ,O00000O0OO0O0OO00 ),4 ,O000O000OOOOO00OO .marker ,1 )#line:226
                cv2 .imshow (O000O000OOOOO00OO .wname ,O000O000OOOOO00OO .img_draw )#line:228
        if O0000000OO0OO00O0 ==cv2 .EVENT_RBUTTONDOWN :#line:231
            if O000O000OOOOO00OO .points .state =='L':#line:233
                cv2 .circle (O000O000OOOOO00OO .img_draw ,(O0O00O0OO000O0OO0 ,O00000O0OO0O0OO00 ),4 ,O000O000OOOOO00OO .marker ,1 )#line:235
                if O000O000OOOOO00OO .line !=None :#line:237
                    O0OO0O0000O00OO0O ,O0O0O0O0OOOO0OO0O =O000O000OOOOO00OO .points .L [-1 ]#line:238
                    cv2 .line (O000O000OOOOO00OO .img_draw ,(O0OO0O0000O00OO0O ,O0O0O0O0OOOO0OO0O ),(O0O00O0OO000O0OO0 ,O00000O0OO0O0OO00 ),O000O000OOOOO00OO .line )#line:239
                O000O000OOOOO00OO .points .add (O0O00O0OO000O0OO0 ,O00000O0OO0O0OO00 ,'R')#line:241
                cv2 .imshow (O000O000OOOOO00OO .wname ,O000O000OOOOO00OO .img_draw )#line:243
                if O000O000OOOOO00OO .mode =='multi':#line:246
                    O000O000OOOOO00OO .points_set .append (O000O000OOOOO00OO .points .points )#line:247
                    O000O000OOOOO00OO .points =pointlist ()#line:248
            else :#line:251
                pass #line:252
            if O000O000OOOOO00OO .mode =='single':#line:255
                cv2 .destroyWindow ('aaa')#line:256
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
