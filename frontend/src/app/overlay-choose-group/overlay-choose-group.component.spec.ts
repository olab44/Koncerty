import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OverlayChooseGroupComponent } from './overlay-choose-group.component';

describe('OverlayChooseGroupComponent', () => {
  let component: OverlayChooseGroupComponent;
  let fixture: ComponentFixture<OverlayChooseGroupComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [OverlayChooseGroupComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(OverlayChooseGroupComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
