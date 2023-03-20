#include "../include/common.h"

int* drawString(int* dl, int style, float x, float y, char* str) {
	float height = (float)getTextStyleHeight(style);
	float text_y = y - (height * 0x5);
	int* dl_copy = displayText(dl, style, 4 * x, 4 * text_y, str, 0);
	return dl_copy;
}

int* colorText(unsigned char* dl, int red, int green, int blue, int opacity) {
	*(unsigned char*)(dl + 0x4) = red;
	*(unsigned char*)(dl + 0x5) = green;
	*(unsigned char*)(dl + 0x6) = blue;
	*(unsigned char*)(dl + 0x7) = opacity;
	return (int*)dl;
}

int* drawText(int* dl, int style, float x, float y, char* str, int red, int green, int blue, int opacity) {
	dl = initDisplayList(dl);
	if (style == 1) {
		*(unsigned int*)(dl + 0) = 0xFCFFFFFF;
		*(unsigned int*)(dl + 1) = 0xFFFCF279;
		*(unsigned int*)(dl + 2) = 0xDA380003;
		*(unsigned int*)(dl + 3) = 0x807FDAC0;
		dl += 4;
	} else {
		*(unsigned int*)(dl + 0) = 0xDE000000; // G_DL 0
		*(unsigned int*)(dl + 1) = 0x01000118; // G_VTX 0 11
		*(unsigned int*)(dl + 2) = 0xFC119623; // G_SETCOMBINE
		*(unsigned int*)(dl + 3) = 0xFF2FFFFF; // G_SETCIMG format: 1, 1, -1
		dl += 4;
		if (style == 6) {
			*(unsigned int*)(dl + 0) = 0xDA380003;
			*(unsigned int*)(dl + 1) = (int)&style6Mtx[0];
			dl += 2;
		}
		*(unsigned int*)(dl + 0) = 0xFA000000; // G_SETPRIMCOLOR
		dl = colorText((unsigned char*)dl,red,green,blue,opacity);
		dl += 2;
	}
	dl = drawString(dl,style,x,y,str);
	return dl;
}

int* drawTextContainer(int* dl, int style, float x, float y, char* str, int red, int green, int blue, int opacity, int background) {
	if (background) {
		int offset = 1;
		dl = drawText(dl,style,x-offset,y+offset,str,0,0,0,0xFF);
	}
	dl = drawText(dl,style,x,y,str,red,green,blue,0xFF);
	return dl;
}

int* drawImage(int* dl, int text_index, codecs codec_index, int img_width, int img_height, int x, int y, float xScale, float yScale, int opacity) {
	dl = initDisplayList(dl);
	*(unsigned int*)(dl++) = 0xE200001C;
	*(unsigned int*)(dl++) = 0x00504240;
	*(unsigned int*)(dl++) = 0xFA000000;
	*(unsigned int*)(dl++) = 0xFFFFFF00 | opacity; // Last 2 bits == Opacity
	*(unsigned int*)(dl++) = 0xFCFF97FF;
	*(unsigned int*)(dl++) = 0xFF2CFE7F;
	*(unsigned int*)(dl++) = 0xE3001201;
	*(unsigned int*)(dl++) = 0x00000000;
	dl = displayImage(dl++, text_index, 0, codec_index, img_width, img_height, x, y, xScale, yScale, 0, 0.0f);
	return dl;
};