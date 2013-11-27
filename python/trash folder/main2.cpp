#include <iostream>
#include <cv.h>
#include <highgui.h>
#include<opencv2/core/core.hpp>
#include<opencv2/highgui/highgui.hpp>
#include<opencv2/imgproc/imgproc.hpp>
#include<opencv2/features2d/features2d.hpp>
#include<sys/time.h>

using namespace std;
using namespace cv;

int main()
{
    vector<KeyPoint> keypoints1, keypoints2;
    Mat descriptors1, descriptors2;
    vector<DMatch> matches;
    
    Mat frame, gray1;
    FastFeatureDetector detector(10);
    FREAK extractor;
    
    BFMatcher matcher(NORM_HAMMING,1);
    
    frame = imread("rodents.png", CV_LOAD_IMAGE_COLOR);
    cvtColor(frame,gray1, CV_BGR2GRAY);
    
    
    detector.detect(gray1, keypoints1);
    struct timeval tim;
    gettimeofday(&tim, NULL);
    double t1=tim.tv_sec+(tim.tv_usec/1000000.0);
    int x=100;
    
    while(x--)
        extractor.compute( gray1, keypoints1, descriptors1);
    gettimeofday(&tim, NULL);

    double t2=tim.tv_sec+(tim.tv_usec/1000000.0);
    printf("%.6lf seconds elapsed\n", t2-t1);
    
    cout<<keypoints1.size()<<endl;
    
    return 0;
}
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        