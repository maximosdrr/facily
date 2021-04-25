import { Body, Controller, Delete, Get, Param, Post } from '@nestjs/common';
import { Contest } from 'src/entities/contest.entity';
import { Todo } from 'src/entities/todo.entity';
import { Winners } from 'src/entities/winners.entity';
import { ContestService } from './contest.service';

@Controller('contest')
export class ContestController {
  constructor(private readonly service: ContestService) {}
  @Post('save-contest')
  async saveContestService(@Body() contest: Contest) {
    return this.service.saveContest(contest);
  }

  @Post('save-winners')
  async saveWinners(@Body() winners: Winners[]) {
    return this.service.saveWinners(winners);
  }

  @Post('save-todo')
  async saveTodo(@Body() todo: Todo) {
    return this.service.saveTodo(todo);
  }

  @Get('find/:id')
  async findContest(@Param('id') id: string) {
    if (!id) return {};
    const result =
      id === 'all'
        ? await this.service.findAllContests()
        : await this.service.findOneContest(id);

    return result;
  }

  @Delete('delete/:id')
  delete(@Param('id') id: string) {
    return this.service.deleteContest(id);
  }
}
