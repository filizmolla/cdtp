G21 G91 G94;Start code
G00 Z20
G00 X0 Y0 
G01 Z-19
G01 Z-1 F250 ;FEED RATE
G01 X0 Y0 ;
G01 X0 Y4 ;
G01 X4 Y0 ;
G01 X0 Y-4 ;
G01 X-4 Y0 ;
G01 Z5;
G01 X4 Y0;
G01 Z-5; 
G01 X0 Y4 ;
G01 X3 Y0 ;
G01 X0 Y-4 ;
G01 X-3 Y0 ;
G01 Z5;
G01 X3 Y0;
G01 Z-5; 
G01 X0 Y3 ;
G01 X3 Y0 ;
G01 X0 Y-3 ;
G01 X-3 Y0 ;
G01 Z5;
G01 X0 Y3;
G01 Z-5; 
G01 X0 Y3 ;
G01 X3 Y0 ;
G01 X0 Y-3 ;
G01 X-3 Y0 ;
G01 Z5;
G01 X-7 Y1;
G01 Z-5; 
G01 X0 Y2 ;
G01 X7 Y0 ;
G01 X0 Y-2 ;
G01 X-7 Y0 ;
G01 Z5;
G01 X-7 Y1;
G01 Z-5; 
G00 Z0 F70
M30
