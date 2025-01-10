import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OverlayNewEventComponent } from './overlay-new-event.component';

describe('OverlayNewEventComponent', () => {
  let component: OverlayNewEventComponent;
  let fixture: ComponentFixture<OverlayNewEventComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [OverlayNewEventComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(OverlayNewEventComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
