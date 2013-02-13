#include "CImg.h"
#include "pCell.h"

using namespace cimg_library;

int main(){
        
    CImg<unsigned char> *image = new CImg<unsigned char>("test.jpg");

    PCell test(0, 0, image);
    test.show();

    //CImg<unsigned char> region = image.get_crop(50,50,100,100);
    //image.draw_image(0,0,region,1);
    CImgDisplay main_disp(*image);
    while(!main_disp.is_closed())
        main_disp.wait();

    return 0;
}
