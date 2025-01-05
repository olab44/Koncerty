import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TranslateModule } from '@ngx-translate/core';
import { TopBarComponent } from '../bars/top-bar/top-bar.component';
import { OverlayNewMessageComponent } from '../overlays/overlay-new-message/overlay-new-message.component';
import { GroupInfo } from '../interfaces';
import { SessionStateService } from '../services/session-state/session-state.service';

@Component({
  selector: 'app-message-forum',
  standalone: true,
  imports: [CommonModule, TranslateModule, TopBarComponent, OverlayNewMessageComponent],
  templateUrl: './message-forum.component.html',
  styleUrl: './message-forum.component.css'
})
export class MessageForumComponent {
  group!: GroupInfo
  viewedMessage = {name: "", content: ""}
  visibleOverlayMessage = false

  messages = [
    {name: "Odwołana próba", content: "Próba zaplanowana na 19.12 NIE odbędzie się."},
    {name: "WESOŁYCH ŚWIĄT", content: "Wesołych Świąt!"}
  ]

  constructor(private state: SessionStateService) {
    this.state.currentGroup.subscribe((group) => {
      this.group = group;
    });
  }

  viewMessage(message: any): void {
    this.viewedMessage = message
  }

  toggleOverlayMessage(): void {
    this.visibleOverlayMessage = !this.visibleOverlayMessage
  }
}
