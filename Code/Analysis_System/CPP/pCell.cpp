#include "pCell.h"
#include "CImg.h"

using namespace cimg_library; 
PCell::PCell(int xc, int yc, CImg<unsigned char> *img){
    this->x = xc;
    this->y = yc;
    this->image = img;
}

void PCell::show(){
    int width = GetWidth();
    int height = GetHeight();
    CImg<unsigned char> tmp;
    tmp = (*(this->image)).get_crop(this->x, this->y, this->x + width, this->y + height);

    CImgDisplay main_disp(tmp);
    while(!main_disp.is_closed())
        main_disp.wait();
}   
