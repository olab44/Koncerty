import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OverlayAddCompositionComponent } from './overlay-add-composition.component';

describe('OverlayAddCompositionComponent', () => {
  let component: OverlayAddCompositionComponent;
  let fixture: ComponentFixture<OverlayAddCompositionComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [OverlayAddCompositionComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(OverlayAddCompositionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
