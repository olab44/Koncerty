import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TranslateModule } from '@ngx-translate/core';
import { TopBarComponent } from '../bars/top-bar/top-bar.component';
import { OverlayChooseGroupComponent } from '../overlays/overlay-choose-group/overlay-choose-group.component';
import { OverlayJoinGroupComponent } from '../overlays/overlay-join-group/overlay-join-group.component';
import { OverlayCreateGroupComponent } from '../overlays/overlay-create-group/overlay-create-group.component';

@Component({
  selector: 'app-home-page',
  standalone: true,
  imports: [CommonModule, TranslateModule, TopBarComponent, OverlayChooseGroupComponent, OverlayJoinGroupComponent, OverlayCreateGroupComponent],
  templateUrl: './home-page.component.html',
  styleUrl: './home-page.component.css'
})
export class HomePageComponent {
  visibleOverlayChoose = false
  visibleOverlayJoin = false
  visibleOverlayCreate = false

  toggleOverlayChoose() {
    this.visibleOverlayChoose = !this.visibleOverlayChoose
  }
  toggleOverlayJoin() {
    this.visibleOverlayJoin = !this.visibleOverlayJoin
  }
  toggleOverlayCreate() {
    this.visibleOverlayCreate = !this.visibleOverlayCreate
  }
}
