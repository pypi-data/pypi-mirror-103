import numpy as np #line:2
from copy import deepcopy #line:3
import matplotlib .pyplot as plt #line:4
import cv2 #line:5
def show (OOO0O0OOO00O00OO0 ):#line:7
    plt .figure (figsize =(8 ,8 ))#line:8
    if np .max (OOO0O0OOO00O00OO0 )==1 :#line:10
        plt .imshow (OOO0O0OOO00O00OO0 ,vmin =0 ,vmax =1 )#line:11
    else :#line:12
        plt .imshow (OOO0O0OOO00O00OO0 ,vmin =0 ,vmax =255 )#line:13
    plt .gray ()#line:14
    plt .show ()#line:15
    plt .close ()#line:16
    print ()#line:17
def resize (O0O0OO0O0OOO0OOOO ,O00O000000OOOOOOO ):#line:19
    O0O0O0O00OOO000OO ,O00000O0OOO00O00O =O0O0OO0O0OOO0OOOO .shape [:2 ]#line:21
    if O0O0O0O00OOO000OO <O00000O0OOO00O00O :#line:23
        OO000OO00O00O0O00 =O00O000000OOOOOOO #line:24
        O0O00O00O0O0O0OO0 =int (O0O0O0O00OOO000OO *O00O000000OOOOOOO /O00000O0OOO00O00O )#line:25
        OOOOO000OOOOO0OOO =O00000O0OOO00O00O /O00O000000OOOOOOO #line:26
    else :#line:27
        O0O00O00O0O0O0OO0 =O00O000000OOOOOOO #line:28
        OO000OO00O00O0O00 =int (O00000O0OOO00O00O *O00O000000OOOOOOO /O0O0O0O00OOO000OO )#line:29
        OOOOO000OOOOO0OOO =O0O0O0O00OOO000OO /O00O000000OOOOOOO #line:30
    O0O0OO0O0OOO0OOOO =cv2 .resize (O0O0OO0O0OOO0OOOO ,(OO000OO00O00O0O00 ,O0O00O00O0O0O0OO0 ),interpolation =cv2 .INTER_CUBIC )#line:31
    print ('------------------------------------')#line:33
    print ('resizing in window size ({}, {})'.format (OO000OO00O00O0O00 ,O0O00O00O0O0O0OO0 ))#line:34
    print ('(w, h) = ({}, {})'.format (O00000O0OOO00O00O ,O0O0O0O00OOO000OO ))#line:35
    print ('(w, h) = ({}, {})'.format (OO000OO00O00O0O00 ,O0O00O00O0O0O0OO0 ))#line:36
    return O0O0OO0O0OOO0OOOO ,OOOOO000OOOOO0OOO #line:37
class pointlist ():#line:39
    def __init__ (O0000O0000O0O00OO ):#line:40
        O0000O0000O0O00OO .points =[]#line:41
        O0000O0000O0O00OO .L =[]#line:42
        O0000O0000O0O00OO .R =[]#line:43
        O0000O0000O0O00OO .state =None #line:44
    def add (OOO0O000O00O0O00O ,OO0O0O0OO0OOOOOOO ,OOOOOO0OO00O00000 ,OO000OO0OOOO00OOO ):#line:46
        OOO0O000O00O0O00O .points .append ([OO0O0O0OO0OOOOOOO ,OOOOOO0OO00O00000 ])#line:47
        if OO000OO0OOOO00OOO =='L':#line:48
            OOO0O000O00O0O00O .L .append ([OO0O0O0OO0OOOOOOO ,OOOOOO0OO00O00000 ])#line:49
            OOO0O000O00O0O00O .state ='L'#line:50
        if OO000OO0OOOO00OOO =='R':#line:51
            OOO0O000O00O0O00O .R .append ([OO0O0O0OO0OOOOOOO ,OOOOOO0OO00O00000 ])#line:52
            OOO0O000O00O0O00O .state ='R'#line:53
        print ('points[{}] = ({}, {})'.format (len (OOO0O000O00O0O00O .points )-1 ,OO0O0O0OO0OOOOOOO ,OOOOOO0OO00O00000 ))#line:54
class vcclick :#line:56
    def __init__ (OOOOO00OO0O0O0OO0 ):#line:57
        pass #line:58
    def __del__ (OOOOO000OO0OO00OO ):#line:59
        pass #line:60
    def get_draw (O0OOO0O0OOOO00O00 ,return_size ='original'):#line:62
        if return_size =='original':#line:63
            O0OOO0O0OOOO00O00 .img_draw_original =cv2 .resize (O0OOO0O0OOOO00O00 .img_draw ,O0OOO0O0OOOO00O00 .img_original .shape [:2 ][::-1 ],interpolation =cv2 .INTER_CUBIC )#line:64
            return O0OOO0O0OOOO00O00 .img_draw_original #line:65
        else :#line:66
            return O0OOO0O0OOOO00O00 .img_draw #line:67
    def get_mask (O00OOO00OOOO000OO ,return_size ='original'):#line:69
        if O00OOO00OOOO000OO .mode =='single':#line:70
            if return_size =='original':#line:71
                OO0O000OOOOOO000O =np .zeros (O00OOO00OOOO000OO .img_original .shape ,int )#line:72
                O0O0OO00OO0O00OO0 =np .array (O00OOO00OOOO000OO .points .points )*O00OOO00OOOO000OO .rate #line:73
                O0O0OO00OO0O00OO0 =O0O0OO00OO0O00OO0 .astype (int )#line:74
                cv2 .fillConvexPoly (OO0O000OOOOOO000O ,points =O0O0OO00OO0O00OO0 ,color =(1 ,1 ,1 ))#line:75
            else :#line:76
                OO0O000OOOOOO000O =np .zeros (O00OOO00OOOO000OO .img .shape ,int )#line:77
                O0O0OO00OO0O00OO0 =np .array (O00OOO00OOOO000OO .points .points )#line:78
                cv2 .fillConvexPoly (OO0O000OOOOOO000O ,points =O0O0OO00OO0O00OO0 ,color =(1 ,1 ,1 ))#line:79
        if O00OOO00OOOO000OO .mode =='multi':#line:80
            if return_size =='original':#line:81
                OO0O000OOOOOO000O =np .zeros (O00OOO00OOOO000OO .img_original .shape ,int )#line:82
                for O0O0000O0O00O0O0O in O00OOO00OOOO000OO .points_set :#line:84
                    O0O0OO00OO0O00OO0 =np .array (O0O0000O0O00O0O0O )*O00OOO00OOOO000OO .rate #line:85
                    O0O0OO00OO0O00OO0 =O0O0OO00OO0O00OO0 .astype (int )#line:86
                    cv2 .fillConvexPoly (OO0O000OOOOOO000O ,points =O0O0OO00OO0O00OO0 ,color =(1 ,1 ,1 ))#line:87
            else :#line:88
                OO0O000OOOOOO000O =np .zeros (O00OOO00OOOO000OO .img .shape ,int )#line:89
                for O0O0000O0O00O0O0O in O00OOO00OOOO000OO .points_set :#line:91
                    O0O0OO00OO0O00OO0 =np .array (O0O0000O0O00O0O0O )#line:92
                    cv2 .fillConvexPoly (OO0O000OOOOOO000O ,points =O0O0OO00OO0O00OO0 ,color =(1 ,1 ,1 ))#line:93
        OO0O000OOOOOO000O =np .sum (OO0O000OOOOOO000O ,axis =2 )==3 #line:94
        return OO0O000OOOOOO000O #line:95
    def single (OO0OOO00O00OOO000 ,OO0O0O0OO000OO0OO ,window_size =1000 ,guide =(0 ,255 ,0 ),marker =(255 ,0 ,0 ),line =(0 ,255 ,0 ),return_size ='original'):#line:101
        OO0OOO00O00OOO000 .img_original =np .array (OO0O0O0OO000OO0OO )#line:103
        OO0OOO00O00OOO000 .window_size =window_size #line:104
        assert guide ==None or len (guide )==3 #line:105
        assert marker ==None or len (marker )==3 #line:106
        assert line ==None or len (line )==3 #line:107
        OO0OOO00O00OOO000 .guide =guide [::-1 ]if guide !=None else None #line:108
        OO0OOO00O00OOO000 .marker =marker [::-1 ]if marker !=None else None #line:109
        OO0OOO00O00OOO000 .line =line [::-1 ]if line !=None else None #line:110
        OO0OOO00O00OOO000 .points =pointlist ()#line:111
        OO0OOO00O00OOO000 .points_set =[]#line:112
        OO0OOO00O00OOO000 .wname ='aaa'#line:113
        OO0OOO00O00OOO000 .img ,OO0OOO00O00OOO000 .rate =resize (OO0OOO00O00OOO000 .img_original ,OO0OOO00O00OOO000 .window_size )#line:116
        OO0OOO00O00OOO000 .h ,OO0OOO00O00OOO000 .w =OO0OOO00O00OOO000 .img .shape [:2 ]#line:118
        OO0OOO00O00OOO000 .img_draw =deepcopy (OO0OOO00O00OOO000 .img )#line:119
        OO0OOO00O00OOO000 .mode ='single'#line:122
        cv2 .namedWindow (OO0OOO00O00OOO000 .wname )#line:123
        cv2 .startWindowThread ()#line:124
        cv2 .setMouseCallback (OO0OOO00O00OOO000 .wname ,OO0OOO00O00OOO000 .start )#line:125
        cv2 .imshow (OO0OOO00O00OOO000 .wname ,OO0OOO00O00OOO000 .img )#line:127
        cv2 .waitKey ()#line:128
        if return_size =='original':#line:131
            print ('return in original size {}'.format (OO0OOO00O00OOO000 .img_original .shape [:2 ][::-1 ]))#line:132
            print ('------------------------------------')#line:133
            return np .array (OO0OOO00O00OOO000 .points .points )*OO0OOO00O00OOO000 .rate #line:134
        else :#line:135
            print ('return in window size {}'.format (OO0OOO00O00OOO000 .img .shape [:2 ][::-1 ]))#line:136
            return np .array (OO0OOO00O00OOO000 .points .points )#line:137
    def multi (OOOO0O0OO00O0OO0O ,O0OO0OOO0O0O0OO0O ,window_size =1000 ,guide =(0 ,255 ,0 ),marker =(255 ,0 ,0 ),line =(0 ,255 ,0 ),return_size ='original'):#line:143
        OOOO0O0OO00O0OO0O .img_original =np .array (O0OO0OOO0O0O0OO0O )#line:145
        OOOO0O0OO00O0OO0O .window_size =window_size #line:146
        assert guide ==None or len (guide )==3 #line:147
        assert marker ==None or len (marker )==3 #line:148
        assert line ==None or len (line )==3 #line:149
        OOOO0O0OO00O0OO0O .guide =guide [::-1 ]if guide !=None else None #line:150
        OOOO0O0OO00O0OO0O .marker =marker [::-1 ]if marker !=None else None #line:151
        OOOO0O0OO00O0OO0O .line =line [::-1 ]if line !=None else None #line:152
        OOOO0O0OO00O0OO0O .points =pointlist ()#line:153
        OOOO0O0OO00O0OO0O .points_set =[]#line:154
        OOOO0O0OO00O0OO0O .wname ='aaa'#line:155
        OOOO0O0OO00O0OO0O .img ,OOOO0O0OO00O0OO0O .rate =resize (OOOO0O0OO00O0OO0O .img_original ,OOOO0O0OO00O0OO0O .window_size )#line:158
        OOOO0O0OO00O0OO0O .h ,OOOO0O0OO00O0OO0O .w =OOOO0O0OO00O0OO0O .img .shape [:2 ]#line:160
        OOOO0O0OO00O0OO0O .img_draw =deepcopy (OOOO0O0OO00O0OO0O .img )#line:161
        OOOO0O0OO00O0OO0O .mode ='multi'#line:164
        cv2 .namedWindow (OOOO0O0OO00O0OO0O .wname )#line:165
        cv2 .startWindowThread ()#line:166
        cv2 .setMouseCallback (OOOO0O0OO00O0OO0O .wname ,OOOO0O0OO00O0OO0O .start )#line:167
        cv2 .imshow (OOOO0O0OO00O0OO0O .wname ,OOOO0O0OO00O0OO0O .img )#line:169
        cv2 .waitKey ()#line:170
        if return_size =='original':#line:173
            print ('return in original size {}'.format (OOOO0O0OO00O0OO0O .img_original .shape [:2 ][::-1 ]))#line:174
            print ('------------------------------------')#line:175
            OOO00000O0OOO0O0O =deepcopy (OOOO0O0OO00O0OO0O .points_set )#line:176
            for OOOOOO0O0OOOO0000 in range (len (OOO00000O0OOO0O0O )):#line:177
                OOO00000O0OOO0O0O [OOOOOO0O0OOOO0000 ]=np .array (OOO00000O0OOO0O0O [OOOOOO0O0OOOO0000 ])*OOOO0O0OO00O0OO0O .rate #line:178
            return OOO00000O0OOO0O0O #line:179
        else :#line:180
            print ('return in window size {}'.format (OOOO0O0OO00O0OO0O .img .shape [:2 ][::-1 ]))#line:181
            OOO00000O0OOO0O0O =deepcopy (OOOO0O0OO00O0OO0O .points_set )#line:182
            for OOOOOO0O0OOOO0000 in range (len (OOO00000O0OOO0O0O )):#line:183
                OOO00000O0OOO0O0O [OOOOOO0O0OOOO0000 ]=np .array (OOO00000O0OOO0O0O [OOOOOO0O0OOOO0000 ])#line:184
            return OOOO0O0OO00O0OO0O .points_set #line:185
    def start (OO00O0OOO0000O0OO ,O0000000OOO0000OO ,O0O0OO0O000O0O0OO ,O0O0O00OOO0O000O0 ,O000OO000OO0OO00O ,O0OO0O00O0O0O00OO ):#line:188
        if O0000000OOO0000OO ==cv2 .EVENT_MBUTTONDOWN and OO00O0OOO0000O0OO .points .state !='L':#line:190
            for OOO00O0OOO0000OO0 in range (1 ,10 ):cv2 .waitKey (1 )#line:191
            cv2 .destroyWindow ('aaa')#line:192
            for OOO00O0OOO0000OO0 in range (1 ,10 ):cv2 .waitKey (1 )#line:193
        if O0000000OOO0000OO ==cv2 .EVENT_MOUSEMOVE :#line:196
            O00OOO00OOOO000O0 =deepcopy (OO00O0OOO0000O0OO .img_draw )#line:198
            if OO00O0OOO0000O0OO .guide !=None :#line:200
                cv2 .line (O00OOO00OOOO000O0 ,(O0O0OO0O000O0O0OO ,0 ),(O0O0OO0O000O0O0OO ,OO00O0OOO0000O0OO .h -1 ),OO00O0OOO0000O0OO .guide )#line:201
                cv2 .line (O00OOO00OOOO000O0 ,(0 ,O0O0O00OOO0O000O0 ),(OO00O0OOO0000O0OO .w -1 ,O0O0O00OOO0O000O0 ),OO00O0OOO0000O0OO .guide )#line:202
            if OO00O0OOO0000O0OO .points .state =='L':#line:204
                if OO00O0OOO0000O0OO .line !=None :#line:205
                    OO0OOO0OOOOO00O0O ,OOOOOO0OO000OOOO0 =OO00O0OOO0000O0OO .points .L [-1 ]#line:206
                    cv2 .line (O00OOO00OOOO000O0 ,(OO0OOO0OOOOO00O0O ,OOOOOO0OO000OOOO0 ),(O0O0OO0O000O0O0OO ,O0O0O00OOO0O000O0 ),OO00O0OOO0000O0OO .guide )#line:207
            cv2 .imshow (OO00O0OOO0000O0OO .wname ,O00OOO00OOOO000O0 )#line:209
        if O0000000OOO0000OO ==cv2 .EVENT_LBUTTONDOWN :#line:212
            if OO00O0OOO0000O0OO .points .state =='L':#line:214
                cv2 .circle (OO00O0OOO0000O0OO .img_draw ,(O0O0OO0O000O0O0OO ,O0O0O00OOO0O000O0 ),4 ,OO00O0OOO0000O0OO .marker ,1 )#line:216
                if OO00O0OOO0000O0OO .line !=None :#line:218
                    OO0OOO0OOOOO00O0O ,OOOOOO0OO000OOOO0 =OO00O0OOO0000O0OO .points .L [-1 ]#line:219
                    cv2 .line (OO00O0OOO0000O0OO .img_draw ,(OO0OOO0OOOOO00O0O ,OOOOOO0OO000OOOO0 ),(O0O0OO0O000O0O0OO ,O0O0O00OOO0O000O0 ),OO00O0OOO0000O0OO .line )#line:220
                OO00O0OOO0000O0OO .points .add (O0O0OO0O000O0O0OO ,O0O0O00OOO0O000O0 ,'L')#line:222
                cv2 .imshow (OO00O0OOO0000O0OO .wname ,OO00O0OOO0000O0OO .img_draw )#line:224
            else :#line:226
                OO00O0OOO0000O0OO .points .add (O0O0OO0O000O0O0OO ,O0O0O00OOO0O000O0 ,'L')#line:228
                cv2 .circle (OO00O0OOO0000O0OO .img_draw ,(O0O0OO0O000O0O0OO ,O0O0O00OOO0O000O0 ),4 ,OO00O0OOO0000O0OO .marker ,1 )#line:230
                cv2 .imshow (OO00O0OOO0000O0OO .wname ,OO00O0OOO0000O0OO .img_draw )#line:232
        if O0000000OOO0000OO ==cv2 .EVENT_RBUTTONDOWN :#line:235
            if OO00O0OOO0000O0OO .points .state =='L':#line:237
                cv2 .circle (OO00O0OOO0000O0OO .img_draw ,(O0O0OO0O000O0O0OO ,O0O0O00OOO0O000O0 ),4 ,OO00O0OOO0000O0OO .marker ,1 )#line:239
                if OO00O0OOO0000O0OO .line !=None :#line:241
                    OO0OOO0OOOOO00O0O ,OOOOOO0OO000OOOO0 =OO00O0OOO0000O0OO .points .L [-1 ]#line:242
                    cv2 .line (OO00O0OOO0000O0OO .img_draw ,(OO0OOO0OOOOO00O0O ,OOOOOO0OO000OOOO0 ),(O0O0OO0O000O0O0OO ,O0O0O00OOO0O000O0 ),OO00O0OOO0000O0OO .line )#line:243
                OO00O0OOO0000O0OO .points .add (O0O0OO0O000O0O0OO ,O0O0O00OOO0O000O0 ,'R')#line:245
                cv2 .imshow (OO00O0OOO0000O0OO .wname ,OO00O0OOO0000O0OO .img_draw )#line:247
                if OO00O0OOO0000O0OO .mode =='multi':#line:250
                    OO00O0OOO0000O0OO .points_set .append (OO00O0OOO0000O0OO .points .points )#line:251
                    OO00O0OOO0000O0OO .points =pointlist ()#line:252
            else :#line:255
                pass #line:256
            if OO00O0OOO0000O0OO .mode =='single':#line:259
                for OOO00O0OOO0000OO0 in range (1 ,10 ):cv2 .waitKey (1 )#line:260
                cv2 .destroyWindow ('aaa')#line:261
                for OOO00O0OOO0000OO0 in range (1 ,10 ):cv2 .waitKey (1 )#line:262
if __name__ =='__main__':#line:265
    file_name ='yoko.JPG'#line:267
    img =cv2 .imread (file_name )#line:272
    show (img )#line:273
    myclick =vcclick ()#line:276
    points =myclick .multi (img )#line:277
    print (points )#line:278
    img_mark =myclick .get_draw ()#line:280
    show (img_mark )#line:281
    mask =myclick .get_mask ()#line:283
    show (mask )#line:284
