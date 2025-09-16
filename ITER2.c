//
//  ITER2.c
//  CS2060CProject
// Rideshare program
//  Created by julian jaramillo
//

#include "ITER2.h"
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <errno.h>


#define MIN_RAND_MINUTES_FACTOR 1.2
#define MAX_RAND_MINUTES_FACTOR 1.5
#define SENTINEL_VALUE -1
#define VACATION_RENTERS 6
#define MIN_MILES 1
#define MAX_MILES 100
#define MIN_RATING 1
#define MAX_RATING 5
#define MAX_CALC 50
#define MIN_CALC .1
//Maximum length of a string
#define  STRING_LENGTH 80
//Two dimensional array storage amounts for rows and columns of survey data
#define SURVEY_RIDER_ROWS 5
#define SURVEY_CATEGORIES 3
// login and sentinel values
#define CORRECT_ID "id1"
#define CORRECT_PASSCODE "ABCD"
#define LOGIN_MAX_ATTEMPTS 3

//RideShare Structure
typedef struct{
    
    double baseFare;
    double costPerMinute;
    double costPerMile;
    double minFlateRate;
    char organizationName[STRING_LENGTH];
    unsigned int surveyCount;
    int survey[SURVEY_RIDER_ROWS][SURVEY_CATEGORIES];
}RideShare;

double getValidDoubleSentinel(int min, int max, int sentinel);
double getValidDouble(int min, int max);
int calculateRandomNumber(int min, int max);
double calculateFare(double base, double cost, double mileCost, double minCharge, double miles, int minutes);
void printFare(int riderCount, double miles, int minutes, double fare);
void fgetsRemoveNewLine(char *stringPtr);
char getYorN();

bool adminLogIn (const char *correctID, const char *correctPassword, unsigned int maxAttempts );
void setUpRideShare(RideShare *rideSharePtr, int min, int max);
bool scanDouble(const char *buffer, double *output);

void displayRideShareRatings(unsigned int *surveyCount, const int survey[][SURVEY_CATEGORIES]);
void getRatings(unsigned int *surveyCount, int survey[][SURVEY_CATEGORIES]);
void riderMode(RideShare *rideShare);

void printSurveyResults(RideShare *RideSharePtr);


int main(void){
    
    RideShare rideShare;
    RideShare *rideSharePtr = &rideShare;
    
    if(adminLogIn(CORRECT_ID, CORRECT_PASSCODE, LOGIN_MAX_ATTEMPTS) == true){
        
        setUpRideShare(rideSharePtr, MIN_CALC, MAX_CALC);
        riderMode(rideSharePtr);
    }
}

//Remove the \n character
void fgetsRemoveNewLine(char *stringPtr){
    
    size_t length = strlen(stringPtr);

    if(stringPtr[length-1] == '\n' && length>0){
        stringPtr[length-1] = '\0';
    }
    else{
        stringPtr[0] = '\0';
    }
}
//adminLogIn function
bool adminLogIn (const char *correctID, const char *correctPassword, unsigned int maxAttempts ){
    
    int attemps = 1;
    bool loggedIn = false;
    char id[STRING_LENGTH];
    char password[STRING_LENGTH];
    
    while(attemps <= maxAttempts && loggedIn == false){
        
        puts("Enter Id: ");
        fgets(id, STRING_LENGTH, stdin );
        fgetsRemoveNewLine(id);
    
        puts("Enter Password: ");
        fgets(password, STRING_LENGTH, stdin );
        fgetsRemoveNewLine(password);
        
        if((strcmp(id, CORRECT_ID) == 0) && (strcmp(password, CORRECT_PASSCODE) == 0)){

                loggedIn = true;
            }
        else{
            puts("Incorrect Id/Passcode");
            attemps++;
            }
        }
    
    return loggedIn;
}
double getValidDouble(int min, int max){
    
    
    bool isValid = false;
    char inputValue[STRING_LENGTH];
    double validDouble = 0;
    //Iterate until valid int is entered
    while(isValid == false){
        
        //store value for valid data input
        fgets(inputValue, STRING_LENGTH, stdin);
        fgetsRemoveNewLine(inputValue);
        
            //Ensures hours are in the range from 0 to max
            if(((scanDouble(inputValue, &validDouble)) && (validDouble >= min) && (validDouble <= max))){
                
                //since valid values set flag to true to exit loop
                isValid = true;
            }
            //Print error for range
            else{
                printf("Error: Not within %d and %d. Please enter the value again.", min, max);
            }
        } //While
      
    return validDouble;
    
}
//Get RideShare info
void setUpRideShare(RideShare *rideSharePtr, int min, int max){
    
    puts("Set up RideShare\n");
    
    puts("Base (or inital) fare = ");
    rideSharePtr->baseFare = getValidDouble(min, max);
    
    puts("Cost per minute = ");
    rideSharePtr->costPerMinute = getValidDouble(min, max);
    
    puts("Cost per mile = ");
    rideSharePtr->costPerMile = getValidDouble(min, max);
    
    puts("Minimum flat rate = ");
    rideSharePtr->minFlateRate = getValidDouble(min, max);
    
    puts("RideShare Organization name = ");
    fgets(rideSharePtr->organizationName,STRING_LENGTH, stdin);
    fgetsRemoveNewLine(rideSharePtr->organizationName);
}
//checks for 'y' or 'n'
char getYorN(){
    
    char inputYorN[2];
    fgets(inputYorN, STRING_LENGTH, stdin);
    
    fgetsRemoveNewLine(inputYorN);
    
    if(strcmp(inputYorN, "y") == 0 || strcmp(inputYorN, "Y") == 0 ){
        
        return 'y';
    }
    else if (strcmp(inputYorN, "n") == 0 || strcmp(inputYorN, "N") == 0){
            
        return 'n';
    }
    else{
        
        puts("Invalid input. Please enter 'y' or 'n'.\n");
        return getYorN();
    }
}
 
bool scanDouble(const char *buffer, double *output){
    
    char *end;
    errno = 0;
    double testNum =0;
    bool isvalid = false;
    
    testNum = strtod(buffer, &end);
    
    if(buffer == end || *end != '\0'){
        isvalid = false;
    }
    else{
        *output = testNum;
        isvalid = true;
    }
    
    return isvalid;
}//ScanDouble

//Returns valid input from user
double getValidDoubleSentinel(int min, int max, int sentinel){
    
    bool isValid = false;
    char inputValue[STRING_LENGTH];
    double validDouble = 0;
    //Iterate until valid int is entered
    while(isValid == false){
        
        puts("Enter the number of miles to your destination: ");
        //store value for valid data input
        fgets(inputValue, STRING_LENGTH, stdin);
        fgetsRemoveNewLine(inputValue);
        
            //Ensures hours are in the range from 0 to max
            if(((scanDouble(inputValue, &validDouble)) && (validDouble >= min) && (validDouble <= max)) || (validDouble == sentinel)){
                
                //since valid values set flag to true to exit loop
                isValid = true;
            }
            //Print error for range
            else{
                printf("Error: Not within %d and %d. Please enter the value again.", min, max);
            }
        } //While
      
    return validDouble;
    
}//GetValidInput
//displaying the rating
void displayRideShareRatings(unsigned int *surveyCount, const int survey[][SURVEY_CATEGORIES]){
    
    puts("Survey Results");

    if(*surveyCount == 0){
        
        puts("No surveys\n");
    }
    else{
        
        puts("Rating Categories:\t1. Safety\t2. Cleanliness\t3. Comfort");
        for(size_t i =0; i < *surveyCount; i++){
            
            printf("Survey %zu:\t", i + 1);
            
            for(size_t j =0; j < SURVEY_CATEGORIES; j++){
                
                printf("%d\t\t", survey[i][j]);
            }
            puts("\n");
        }
    }
}//DisplayRideShareRatings
//getting the ratings
void getRatings(unsigned int *surveyCount, int survey[][SURVEY_CATEGORIES]){
    
    puts("We want to know how your experience was on your ride today. Using the rating system 1 to 5 enter your rating for each category:\n");

    for(size_t i =0; i< SURVEY_CATEGORIES; i++){
        puts("1.Safety\t\t\t2.Cleanliness\t\t\t3.Comfort");
        puts("Enter your rating for\t");
        printf("%zu: ", i+1);
        
        int input = getValidDouble(MIN_RATING, MAX_RATING);
        survey[*surveyCount][i] = input;
           
    }
    (*surveyCount)++;
}//getRatings
//Printing out the survey averages
void printSurveyResults(RideShare *RideSharePtr){
    //if no surveys are taken
    if(RideSharePtr->surveyCount == 0){
        
        printf("There are no averages\n");
        
    }
    else{
        
        double average[SURVEY_CATEGORIES];
        
        for(int i = 0; i < SURVEY_CATEGORIES; i++){
            
            double numSum = 0;
            for(int j =0; j < RideSharePtr->surveyCount; j++){
                
                numSum += RideSharePtr->survey[j][i];
                
            }//1stfor
            
            average[i] = numSum/RideSharePtr->surveyCount;
            
        }//2ndfor
        puts("Category Rating Averages\n");
        puts("1.Safety\t\t\t2.Cleanliness\t\t\t3.Comfort");
        
        for(int j = 0; j < SURVEY_CATEGORIES; j++){
            
           printf("%.1lf\t\t\t",average[j]);
        }
    }
}//SurveyResults
//Rider mode
void riderMode(RideShare *rideSharePtr){
    
    int totalRiders = 0;
    double totalMiles = 0;
    double totalMinutes = 0;
    double totalFare = 0;
    bool flagLogIn = false;
    rideSharePtr->surveyCount = 0;
    do {
        printf("Welcome to the %s. We can only provide services for rides from 1 to 100 miles.", rideSharePtr->organizationName);
        
        displayRideShareRatings(&(rideSharePtr->surveyCount), rideSharePtr->survey);
        
        printf("Do you want to request a ride from %s?", rideSharePtr->organizationName);
        char answer = getYorN();
        
        if(answer == 'y'){
            puts("Enter the number of miles to your destination:\n");
            double currentMiles = getValidDoubleSentinel(MIN_MILES, MAX_MILES, SENTINEL_VALUE);
            
            if(currentMiles == SENTINEL_VALUE){
                
                if( adminLogIn(CORRECT_ID, CORRECT_PASSCODE, LOGIN_MAX_ATTEMPTS) == true){
                    
                    puts("Admin shutdown. Exiting RideShare Mode");
                    
                    printf("%s Summary Report\n", rideSharePtr->organizationName);
                    printFare(totalRiders, totalMiles, totalMinutes, totalFare);
                    printSurveyResults(rideSharePtr);
                    flagLogIn = true;
                    
                }
            }
            else{
                
                //Vars for calculation
                unsigned int randMin = 0;
                unsigned int randMax = 0;
                unsigned int currentMinetes = 0;
                double currentFare = 0;
                //Calculate random minute max and min
                randMin = MIN_RAND_MINUTES_FACTOR * currentMiles;
                randMax = MAX_RAND_MINUTES_FACTOR * currentMiles;

                //calculate random minutes and fare
                currentMinetes = calculateRandomNumber(randMin, randMax);
                currentFare = calculateFare(rideSharePtr->baseFare, rideSharePtr->costPerMinute, rideSharePtr->costPerMile, rideSharePtr->minFlateRate, currentMiles, currentMinetes);
                
                //calculate totals
                totalMiles+= currentMiles;
                totalMinutes += currentMinetes;
                totalFare += currentFare;
                totalRiders++;
                
                //Print ride info
                puts("Current Ride Information\n");
                printFare(totalRiders, currentMiles, currentMinetes, currentFare);
                
                puts("Do you want to rate your rideshare experience?");
                char answer2 = getYorN();
                
                if(answer2 == 'n'){
                    
                    puts("Thanks for riding with us");
                }
                else{
                    
                    getRatings(&(rideSharePtr->surveyCount),rideSharePtr->survey);
                }
                
            }
            
        }
        
    }while (flagLogIn == false);
}//RiderMode

//calculates rider fare
double calculateFare(double base, double cost, double mileCost, double minCharge, double miles, int minutes){
    
    //formula to calculate fare
    double fare = base + (cost * minutes) + (mileCost * miles);
    
    //check if minum rate reached
    if(fare <= minCharge){
        
        fare = minCharge;
    }
    return fare;
                                                   
}//CalculateFare

//calculate random number
int calculateRandomNumber(int min, int max){
    
    int randomNum = rand() % (max-min+1) + min;
    return randomNum;
}//RandomNumber


//prints the riders, miles, minutes and fare
void printFare(int riderCount, double miles, int minutes, double fare){
    
    puts("");
    if(riderCount ==0){
        
        puts("There were no riders");
    }
    else{
        
        puts("Rider \tNumber of Miles     Number of Minutes     Rider Fare Amount");
        printf("%d  \t %.1lf                 %d                    $%.2lf\n\n", riderCount, miles, minutes, fare);
    }
}//PrintFare
