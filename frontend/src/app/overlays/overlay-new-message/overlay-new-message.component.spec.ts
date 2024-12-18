import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OverlayNewMessageComponent } from './overlay-new-message.component';

describe('OverlayNewMessageComponent', () => {
  let component: OverlayNewMessageComponent;
  let fixture: ComponentFixture<OverlayNewMessageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [OverlayNewMessageComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(OverlayNewMessageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
