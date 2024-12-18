import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TranslateModule } from '@ngx-translate/core';
import { TopBarComponent } from '../bars/top-bar.component';
import { OverlayAddCompositionComponent } from '../overlays/overlay-add-composition/overlay-add-composition.component';

@Component({
  selector: 'app-music-catalogue',
  standalone: true,
  imports: [ CommonModule, TranslateModule, TopBarComponent, OverlayAddCompositionComponent ],
  templateUrl: './music-catalogue.component.html',
  styleUrl: './music-catalogue.component.css'
})
export class MusicCatalogueComponent {
  group: any
  viewedComposition = {title: "", author: ""}
  visibleOverlayComposition = false

  compositions = [
    {title: "We'll be fine", author: "Jorge Rivera-Herrans"}
  ]

  constructor() {
    this.group = history.state.group;
  }

  viewComposition(composition: any): void {
    this.viewedComposition = composition
  }

  toggleOverlayComposition(): void {
    this.visibleOverlayComposition = !this.visibleOverlayComposition
  }
}
