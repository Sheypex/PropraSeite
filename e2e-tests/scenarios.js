'use strict';

/* https://github.com/angular/protractor/blob/master/docs/toc.md */

describe('my app', function() {


  it('should automatically redirect to /homeView when location hash/fragment is empty', function() {
    browser.get('index.html');
    expect(browser.getLocationAbsUrl()).toMatch("/homeView");
  });


  describe('homeView', function() {

    beforeEach(function() {
      browser.get('index.html#!/homeView');
    });


    it('should render homeView when user navigates to /homeView', function() {
      expect(element.all(by.css('[ng-view] p')).first().getText()).
        toMatch(/partial for view 1/);
    });

  });


  describe('moreInfoView', function() {

    beforeEach(function() {
      browser.get('index.html#!/moreInfoView');
    });


    it('should render moreInfoView when user navigates to /moreInfoView', function() {
      expect(element.all(by.css('[ng-view] p')).first().getText()).
        toMatch(/partial for view 2/);
    });

  });
});
