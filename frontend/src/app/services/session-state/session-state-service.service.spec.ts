import { TestBed } from '@angular/core/testing';

import { SessionStateServiceService } from './session-state-service.service';

describe('SessionStateServiceService', () => {
  let service: SessionStateServiceService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(SessionStateServiceService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
