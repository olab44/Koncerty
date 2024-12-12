import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MessageForumComponent } from './message-forum.component';

describe('MessageForumComponent', () => {
  let component: MessageForumComponent;
  let fixture: ComponentFixture<MessageForumComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MessageForumComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(MessageForumComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
