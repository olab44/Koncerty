import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TranslateModule } from '@ngx-translate/core';
import { TopBarComponent } from '../bars/top-bar.component';

@Component({
  selector: 'app-message-forum',
  standalone: true,
  imports: [CommonModule, TranslateModule, TopBarComponent],
  templateUrl: './message-forum.component.html',
  styleUrl: './message-forum.component.css'
})
export class MessageForumComponent {
  group: any
    viewedMessage: any
  visibleOverlayMessage = false

  messages = [
    {name: "Odwołana próba", content: "Próba zaplanowana na 19.12 NIE odbędzie się."},
    {name: "WESOŁYCH ŚWIĄT", content: "Wesołych świąt! I szczęśliwego Nowego Roku."}
  ]

  constructor() {
    this.group = history.state.group;
  }

  viewMessage(message: any): void {
    this.viewedMessage = message
    console.log(message.content)
  }

  toggleOverlayMessage(): void {
    this.visibleOverlayMessage = !this.visibleOverlayMessage
  }
}
