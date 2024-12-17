import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OverlayJoinGroupComponent } from './overlay-join-group.component';

describe('OverlayJoinGroupComponent', () => {
  let component: OverlayJoinGroupComponent;
  let fixture: ComponentFixture<OverlayJoinGroupComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [OverlayJoinGroupComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(OverlayJoinGroupComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
