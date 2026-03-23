Feature: Movie Theater Booking
    As a Movie enthusiast
    I want to browse different moives
    So that I can book seats for movies I want to go to

    Scenario: User can successfully login
        Given I am on the login page
        When I enter valid credentials
        Then I should be redirected to the movie listing page
    
    Scenario: User cannot login with invalid credentials
        Given I am on the login page
        When I enter invalid credentials
        Then I should see a login error
    
    Scenario: User can view the movie listing page
        Given there are movies in the database
        When I navigate to the movie listing page
        Then I should see a 200 status code

    Scenario: User can view available seats for a movie
        Given there are movies in the database
        When I navigate to the seat booking page
        Then I should see a 200 status code

    Scenario: User can view the booking history page
        Given I am in the app
        When I navigate to the booking history page
        Then I should see a 200 status code

    Scenario: User can successfully book an available seat
        Given there are movies in the database
        And there is an available seat
        And I am logged in
        When I book the seat
        Then the seat should be marked as booked

    Scenario: User cannot book a seat that is already taken
        Given there are movies in the database
        And there is an unavailable seat
        When I choose a seat that is unavailable
        Then I should see a seat already booked error
        