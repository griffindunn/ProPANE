#include "CImg.h"

using namespace cimg_library;



class PCell{

private:
    static int cell_width;
    static int cell_height;

    int x;
    int y;

    CImg<unsigned char> *image;
    
public:
    // Constructors
    PCell(int xc, int yc, CImg<unsigned char> *img);


    // Static methods
    static void setWidthHeight(int width, int height){
        cell_width = width;
        cell_height = height;
    }

    static int GetWidth(void){ return cell_width;}

    static int GetHeight(void){return cell_height;}


    // Instance methods
    void show();

};

int PCell::cell_width = 0;
int PCell::cell_height = 0;
