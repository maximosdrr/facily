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

  @Post('find-all-lines-that-contains-sequence')
  findAllLinesThatContainsSequence(
    @Body() data: { sequence: number[]; type: string },
  ) {
    return this.service.findAllLinesThatContainSequence(
      data.sequence,
      data.type,
    );
  }

  @Post('find-sequence-ocurrence')
  findSequenceOcurrence(@Body() data: { sequence: number[]; type: string }) {
    return this.service.findSequenceOcurrence(data.sequence, data.type);
  }

  @Post('find-sequence-pontuation')
  findSequencePontuation(@Body() data: { sequence: number[]; type: string }) {
    return this.service.findSequencePontuation(data.sequence, data.type);
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
