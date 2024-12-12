import { Component } from '@angular/core';
import { TopBarComponent } from '../top-bar/top-bar.component';

@Component({
  selector: 'app-message-forum',
  standalone: true,
  imports: [TopBarComponent],
  templateUrl: './message-forum.component.html',
  styleUrl: './message-forum.component.css'
})
export class MessageForumComponent {

}
