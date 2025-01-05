import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SideBarEventComponent } from './side-bar-event.component';

describe('SideBarEventComponent', () => {
  let component: SideBarEventComponent;
  let fixture: ComponentFixture<SideBarEventComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SideBarEventComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SideBarEventComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
