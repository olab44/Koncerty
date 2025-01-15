import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TranslateModule } from '@ngx-translate/core';
import { Router } from '@angular/router';
import { TopBarComponent } from '../bars/top-bar/top-bar.component';
import { OverlayNewMessageComponent } from '../overlays/overlay-new-message/overlay-new-message.component';
import { GroupInfo, UserInfo } from '../interfaces';
import { SessionStateService } from '../services/session-state/session-state.service';
import { BackendService } from '../services/backend-connection/backend.service';  // Import BackendService

@Component({
  selector: 'app-message-forum',
  standalone: true,
  imports: [CommonModule, TranslateModule, TopBarComponent, OverlayNewMessageComponent],
  templateUrl: './message-forum.component.html',
  styleUrls: ['./message-forum.component.css']
})
export class MessageForumComponent implements OnInit {
  group!: GroupInfo;
  user!: UserInfo; // User info added
  viewedMessage = {name: "", content: ""};
  visibleOverlayMessage = false;
  messages: any[] = [];  // Adjust type as per the backend response

  constructor(private router: Router, private backend: BackendService, private state: SessionStateService) {
    // Fetch group from the service as before
    this.state.currentGroup.subscribe((group) => {
      this.group = group;
    });
  }

  ngOnInit(): void {
    this.fetchMessages();
  }

  fetchMessages(): void {
    const request = {
        parent_group: this.group.group_id,  // Use group_id for parent_group
    };

    this.backend.getAlerts(request.parent_group)  // Only send parent_group
      .subscribe((response) => {
        console.log('Fetched alerts:', response);
        this.messages = response.alerts || [];  // Assign fetched data to messages array
      }, (error) => {
        console.error('Error fetching alerts', error);
      });
}

  
  
  
  viewMessage(message: any): void {
    this.viewedMessage = { name: message.name, content: message.content };
  }

  toggleOverlayMessage(): void {
    this.visibleOverlayMessage = !this.visibleOverlayMessage;
  }
}
