import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OverlayCreateGroupComponent } from './overlay-create-group.component';

describe('OverlayCreateGroupComponent', () => {
  let component: OverlayCreateGroupComponent;
  let fixture: ComponentFixture<OverlayCreateGroupComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [OverlayCreateGroupComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(OverlayCreateGroupComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
